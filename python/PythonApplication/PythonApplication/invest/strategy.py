import b_sig
import s_sig
import util
import common
import datetime
import time
import enum
from pprint import pprint
from stk_data import get_real_time_quo, day_bars
import quotool

logger = util.get_logger()


class ExeAction(enum.IntEnum):
    Buy = 0
    Sell = 1


class MyStrategy:
    def __init__(self):
        self.have_sell = False
        self.have_buy = False

        self._check_config()
        self._check_table()
        self._download_day_bar()

    @staticmethod
    def _check_config():
        """
        config check
        """
        logger.info('config check')

        assert isinstance(util.get_config('strategy', 'buy_sig_weight'), dict), \
        'buy_sig_weight is not dict'
        assert isinstance(util.get_config('strategy', 'sell_sig_weight'), dict), \
        'sell_sig_weight is not dict'
        assert isinstance(util.get_config('strategy', 'index_sell_sig_weight'), dict), \
        'index_sell_sig_weight is not dict'
        assert util.get_config('strategy', 'index'), \
        'index is null'
        assert util.get_config('strategy', 'pool') and isinstance(util.get_config('strategy', 'pool'), list), \
        'pool is null or is not list'
        assert util.get_config('strategy', 'stop_loss') <= 0, \
        'stop_loss gt 0'
        assert util.get_config('strategy', 'take_profit') >= 0, \
        'take_profit lt 0'
        assert util.get_config('strategy', 'max_hold_day') >= 0, \
        'max_hold_day lt 0'
        assert util.get_config('strategy', 'trailing_loss') <= 0, \
        'trailing_loss gt 0'
        assert util.get_config('strategy', 'before_close_sell') is not None, \
        'before_close_sell is null'
        assert util.get_config('strategy', 'before_close_buy') is not None, \
        'before_close_buy is null'

        logger.info('config check ok')

    @staticmethod
    def _check_table():
        """
        table check
        """
        logger.info('table check')

        db = util.get_mysql('test')

        db.execute('SELECT 1 FROM `config`')
        db.execute('SELECT 1 FROM `code_pool`')
        db.execute('SELECT 1 FROM `position`')
        db.execute('SELECT 1 FROM `holidays`')

        logger.info('table check ok')

    @staticmethod
    def _download_day_bar():
        """
        download day bar
        """
        all_pos = common.get_all_pos()
        all_symbol = [pos['symbol'] for pos in all_pos]

        pools = util.get_config('strategy', 'pool')
        for pool in pools:
            all_symbol.extend(common.get_stock_pool(pool))

        all_symbol = set(all_symbol)

        for symbol in all_symbol:
            quotool.his_quo(symbol)

        quotool.his_quo(util.get_config('strategy', 'index'), is_index=True)
        
    @staticmethod
    def buy_sig(symbol):
        """
        buy sig
        :return:
        """
        indicator = util.get_config('strategy', 'buy_sig_weight')

        buy_sig = {}
        score = 0

        for ind, weight in indicator.items():
            logger.info(f"cal... {ind}")

            sig_func = getattr(b_sig, ind, None)

            if not callable(sig_func):
                logger.warning(f"{ind} not callable")
                continue
            if weight == 0:
                continue

            is_sig = sig_func(symbol)

            score += (weight if is_sig else 0)
            buy_sig[ind] = is_sig

        return buy_sig, score

    @staticmethod
    def sell_sig(symbol):
        """
        sell sig
        :return:
        """
        indicator = util.get_config('strategy', 'sell_sig_weight')

        sell_sig = {}
        score = 0

        for ind, weight in indicator.items():
            logger.info(f"cal... {ind}")

            sig_func = getattr(s_sig, ind, None)

            if not callable(sig_func):
                logger.warning(f"{ind} not callable")
                continue
            if weight == 0:
                continue

            is_sig = sig_func(symbol)

            score += (weight if is_sig else 0)
            sell_sig[ind] = is_sig

        return sell_sig, score

    @staticmethod
    def index_sig():
        """
        index trending
        :return:
        """
        indicator = util.get_config('strategy', 'index_sell_sig_weight')
        index = util.get_config('strategy', 'index')

        sell_sig = {}
        score = 0

        for ind, weight in indicator.items():
            logger.info(f"cal... {ind}")

            sig_func = getattr(s_sig, ind, None)

            if not callable(sig_func):
                logger.warning(f"{ind} not callable")
                continue
            if weight == 0:
                continue

            is_sig = sig_func(index)

            score += (weight if is_sig else 0)
            sell_sig[ind] = is_sig

        return {'index': [
            {
                'symbol': index,
                'score': -score,
                's_sig': sell_sig
            }
        ]}

    def predict(self, symbol):
        """
        product a predict value
        :param symbol:
        :return:
        """
        buy_sig, b_score = self.buy_sig(symbol)
        sell_sig, s_score = self.sell_sig(symbol)

        buy_sig = sorted(list(buy_sig.items()), key=lambda x: x[1], reverse=True)
        sell_sig = sorted(list(sell_sig.items()), key=lambda x: x[1], reverse=True)

        total_score = b_score - s_score

        return {
            'symbol': symbol,
            'score': total_score,
            'b_sig': buy_sig,
            's_sig': sell_sig
        }

    def sector_rank(self):
        """
        rank of sector
        :return:
        """
        pools = util.get_config('strategy', 'pool')
        sector = {}

        for pool in pools:
            rank_list = []
            symbol_list = common.get_stock_pool(pool)

            for symbol in symbol_list:
                prd = self.predict(symbol)
                rank_list.append(prd)

            rank_list.sort(key=lambda x: x['score'], reverse=True)
            sector[pool] = rank_list

        return sector

    def stop_loss(self, pos):
        """
        stop loss
        :return:
        """
        quo = get_real_time_quo(pos['symbol'])
        last_price = float(quo['price'].iloc[0])

        if last_price <= 0:
            logger.error(f"{pos['symbol']} last price({last_price}) abnormal")
            return False
        if pos['avgprice'] <= 0:
            logger.error(f"{pos['avgprice']} last price({pos['avgprice']}) abnormal")
            return False

        pos_rtn =  last_price / pos['avgprice'] - 1

        logger.info(f"{pos['symbol']} avg price: {pos['avgprice']}, last price: {last_price}, "
                    f" return: {pos_rtn}")

        if pos_rtn <= util.get_config('strategy', 'stop_loss'):
            return True

        return False

    def take_profit(self, pos):
        """
        take profit
        :return:
        """
        quo = get_real_time_quo(pos['symbol'])
        last_price = float(quo['price'].iloc[0])

        if last_price <= 0:
            logger.error(f"{pos['symbol']} last price({last_price}) abnormal")
            return False
        if pos['avgprice'] <= 0:
            logger.error(f"{pos['avgprice']} last price({pos['avgprice']}) abnormal")
            return False

        pos_rtn = last_price / pos['avgprice'] - 1

        logger.info(f"{pos['symbol']} avg price: {pos['avgprice']}, last price: {last_price}, "
                    f" return: {pos_rtn}")

        if pos_rtn >= util.get_config('strategy', 'take_profit'):
            return True

        return False

    def max_hold_day_sell(self, pos):
        """
        sell if reach max hold day
        """
        addpos_date = str(pos['lastaddpostime'])[:10]
        today = str(datetime.datetime.today().date())

        hold_day = util.traday_diff(addpos_date, today)

        logger.info(f"{pos['symbol']} hold day: {hold_day}")
        
        if hold_day >= util.get_config('strategy', 'max_hold_day'):
            return True

        return False

    def trailing_stop(self, pos):
        """
        trailing stop
        :param pos:
        :return:
        """
        day_line_bars = day_bars(pos['symbol'], num=60)
        addpos_date = str(pos['lastaddpostime'])[:10]

        day_closes = [bar['close'] for bar in day_line_bars if bar['date'] >= addpos_date]
        max_close = max(day_closes)

        quo = get_real_time_quo(pos['symbol'])
        last_price = float(quo['price'].iloc[0])

        if last_price <= 0:
            logger.error(f"{pos['symbol']} last price({last_price}) abnormal")
            return False

        stop_price = max_close * (1 + util.get_config('strategy', 'trailing_loss'))

        logger.info(f"{pos['symbol']} max close: {max_close},"
                    f" stop price: {stop_price}, last price: {last_price}")

        if stop_price >= last_price:
            return True

        return False

    def sell(self):
        """
        sell
        :return:
        """
        all_pos = common.get_all_pos()

        sell_list = []

        for pos in all_pos:
            sell_reason = ''

            if self.stop_loss(pos):
                sell_reason = 'stop loss'
            elif self.take_profit(pos):
                sell_reason = 'take profit'
            elif self.max_hold_day_sell(pos):
                sell_reason = 'max hold day'
            elif self.trailing_stop(pos):
                sell_reason = 'trailing stop'

            if sell_reason:
                sell_list.append(f"{pos['symbol']} | {sell_reason}")

        return sell_list

    def is_time_exe(self, action=None):
        """
        if it is time to execute
        """
        if action == ExeAction.Sell:
            exe_time = common.get_openclose_time()[1] - \
             util.get_config('strategy', 'before_close_sell') * 60
            now = time.time()
            if now >= exe_time:
                return True
        elif action == ExeAction.Buy:
            exe_time = common.get_openclose_time()[1] - \
             util.get_config('strategy', 'before_close_buy') * 60
            now = time.time()
            if now >= exe_time:
                return True

        return False

    def buy(self):
        """
        buy
        :return:
        """
        sig_info = {}

        symbol_rank = self.sector_rank()
        sig_info.update(symbol_rank)

        index_sig = self.index_sig()
        sig_info.update(index_sig)

        return sig_info

    def run(self):
        """
        run
        :return:
        """
        if not self.have_sell and self.is_time_exe(ExeAction.Sell):
            self.have_sell = True

            sell_list = self.sell()
            sell_info = '\n'.join(sell_list)
            print(sell_info)

        if not self.have_buy and self.is_time_exe(ExeAction.Buy):
            self.have_buy = True

            buy_info = self.buy()
            pprint(buy_info)

            logger.info("strategy completed")

        return self.have_buy


if __name__ == '__main__':
    pass

