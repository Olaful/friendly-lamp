import b_sig
import s_sig
import util
import common
import datetime
from pprint import pprint
from stk_data import get_real_time_quo, day_bars

logger = util.get_logger()


class MyStrategy:
    def __init__(self):
        pass

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
        if pos['avg_price'] <= 0:
            logger.error(f"{pos['avg_price']} last price({pos['avg_price']}) abnormal")
            return False

        pos_rtn = pos['avg_price'] / last_price - 1

        logger.info(f"{pos['symbol']} avg price: {pos['avg_price']}, last price: {last_price}, "
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
        if pos['avg_price'] <= 0:
            logger.error(f"{pos['avg_price']} last price({pos['avg_price']}) abnormal")
            return False

        pos_rtn = pos['avg_price'] / last_price - 1

        logger.info(f"{pos['symbol']} avg price: {pos['avg_price']}, last price: {last_price}, "
                    f" return: {pos_rtn}")

        if pos_rtn >= util.get_config('strategy', 'take_profit'):
            return True

        return False

    def max_hold_day_sell(self, pos):
        """
        sell if reach max hold day
        """
        addpos_date = str(pos['addpos_date'])[:10]
        today = str(datetime.datetime.today().date())

        hold_day = util.traday_diff(addpos_date, today)
        
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
        addpos_date = str(pos['addpos_date'])[:10]

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
            if self.take_profit(pos):
                sell_reason = 'take profit'
            if self.max_hold_day_sell(pos):
                sell_reason = 'max hold day'
            if self.trailing_stop(pos):
                sell_reason = 'trailing stop'

            if sell_reason:
                sell_list.append(f"{pos['symbol']} | {sell_reason}")

        return sell_list

    def buy(self):
        """
        buy
        :return:
        """

    def run(self):
        """
        run
        :return:
        """
        sig_info = {}

        symbol_rank = self.sector_rank()
        sig_info.update(symbol_rank)

        index_sig = self.index_sig()
        sig_info.update(index_sig)

        pprint(sig_info)


if __name__ == '__main__':
    pass

