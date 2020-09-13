import datetime
import time
import enum
import json
import re
from pprint import pprint

import quotool

from invest.strategy_base import StrategyBase
from invest import util, common, b_sig, s_sig
from invest.stk_data import get_real_time_quo, day_bars

logger = util.get_logger()


class ExeAction(enum.IntEnum):
    Buy = 0
    Sell = 1


class MyStrategy(StrategyBase):
    def __init__(self):
        super().__init__()

        util.init_config('strategy', from_db=True)

        self.have_sell = False
        self.have_buy = False

        self._buy_reason = []
        self._sell_reason = []

        self.check_config()
        self._download_day_bar()

    @classmethod
    def name(cls):
        return 'ms'

    @property
    def cfg_name(self):
        return 'strategy'

    @property
    def pools(self):
        return util.get_config('strategy', 'pool')

    @property
    def buy_info(self):
        """
        buy info
        """
        re_score = re.compile('score:(?P<score>.*?),')
        total_score = 0
        buy_reason = []

        for b_r in self._buy_reason:
            search_obj = re_score.search(b_r)
            score = float(search_obj.group('score'))
            total_score += score

            buy_reason.append([score, search_obj.start(), b_r])

        buy_reason.sort(key=lambda x: x[0], reverse=True)

        b_reason = []

        for b_r in buy_reason:
            weight_percent = round(b_r[0] / total_score, 4) * 100

            front_text = b_r[2][:b_r[1]]
            tail_text = b_r[2][b_r[1]:]
            mid_text = f"ca_wei: {weight_percent}%, "
            full_text = ''.join([front_text, mid_text, tail_text])

            b_reason.append(full_text)

        buy_info = '\n'.join(b_reason)
            
        return buy_info

    def check_config(self):
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

            if rank_list:
                sector[pool] = rank_list

        return sector

    def record_sell_info(self, symbol, sell_type, **remark):
        """
        record the info of sell
        """
        if len(self._sell_reason) > util.get_config('strategy', 'max_pos'):
            self._sell_reason.clear()

        rmk = {}
        rmk['symbol'] = symbol
        rmk['type'] = sell_type
        rmk.update(remark)
        j_remark = json.dumps(rmk)
        j_remark = j_remark.replace('"', '').replace('{', '').replace('}', '')

        self._sell_reason.append(j_remark)

    def record_buy_info(self, symbol, pool, **remark):
        """
        record the info of buy
        """
        if len(self._buy_reason) > util.get_config('strategy', 'max_pos'):
            self._buy_reason.clear()

        rmk = {}
        rmk['symbol'] = symbol
        rmk['pool'] = pool
        rmk.update(remark)
        j_remark = json.dumps(rmk)
        j_remark = j_remark.replace('"', '').replace('{', '').replace('}', '')

        self._buy_reason.append(j_remark)

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
            self.record_sell_info(pos['symbol'], 'stop loss', avg_price=pos['avgprice'], last_price=round(last_price, 2))
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
            self.record_sell_info(pos['symbol'], 'take profit', avg_price=pos['avgprice'], last_price=round(last_price, 2))
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
            self.record_sell_info(pos['symbol'], 'max hold day', addpos_date=addpos_date, hold_day=hold_day)
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
            self.record_sell_info(pos['symbol'], 'trailing stop', addpos_date=addpos_date,
             max_close=max_close, stop_price=round(stop_price, 2), last_price=round(last_price, 2))
            return True

        return False

    def sig_sell(self, pos):
        """
        signal to sell
        """
        sell_sig, s_score = self.sell_sig(pos['symbol'])

        if s_score < util.get_config('strategy', 'sell_sig_threshold'):
            return False

        sig = [s_n for s_n, s in sell_sig.items() if s == True]
        sig_rmk = {}
        sig_rmk['score'] = round(s_score, 4)
        sig_rmk.update({s[3:] if s.startswith('is_') else s:
        util.get_config('strategy', 'sell_sig_weight', s) for s in sig})

        self.record_sell_info(pos['symbol'], 'sell signal', **sig_rmk)

        return True

    def sell(self):
        """
        sell
        :return:
        """
        all_pos = common.get_all_pos()

        for pos in all_pos:
            if self.stop_loss(pos):
                pass
            elif self.take_profit(pos):
                pass
            elif self.max_hold_day_sell(pos):
                pass
            elif self.is_start_trailing_stop(pos['symbol'])\
                    and self.trailing_stop(pos):
                pass
            elif self.sig_sell(pos):
                pass

    def is_start_trailing_stop(self, symbol):
        """
        if start trailing stop
        :return:
        """
        cum_day_rtn_sig = s_sig.is_reach_rtn_3_days(symbol)
        if cum_day_rtn_sig:
            logger.info(f"{symbol} start trailing stop")
            return True

        return False

    def is_time_exe(self, action=None):
        """
        if it is time to execute
        """
        if action == ExeAction.Sell:
            exe_time = common.get_openclose_time()[1] - \
             util.get_config('strategy', 'before_close_sell') * 60
            now = time.time()
            if now >= exe_time:
                logger.info("Time to sell")
                return True
        elif action == ExeAction.Buy:
            exe_time = common.get_openclose_time()[1] - \
             util.get_config('strategy', 'before_close_buy') * 60
            now = time.time()
            if now >= exe_time:
                logger.info("Time to buy")
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

        for pool, symbols in symbol_rank.items():
            top_ones = symbols[:util.get_config('strategy', 'pool_top_num')]
            for top_one in top_ones:
                if top_one['score'] < util.get_config('strategy', 'buy_sig_threshold'):
                    continue

                sig = [s[0] for s in top_one['b_sig'] if s[1] == True]
                sig_rmk = {}
                sig_rmk['score'] = round(top_one['score'], 4)
                sig_rmk.update({s[3:] if s.startswith('is_') else s:
                util.get_config('strategy', 'buy_sig_weight', s) for s in sig})

                self.record_buy_info(top_one['symbol'], pool, **sig_rmk)

        index_sig = self.index_sig()
        sig_info.update(index_sig)

        return sig_info

    def run(self):
        """
        run
        :return:
        """
        if self.have_buy:
            return

        if not self.have_sell and self.is_time_exe(ExeAction.Sell):
            self.have_sell = True

            self.sell()
            sell_info = '\n'.join(self._sell_reason)
            print(sell_info)

            if sell_info and util.get_config('strategy', 'is_mail'):
                util.send_mail('m_s', sell_info)

        if not self.have_buy and self.is_time_exe(ExeAction.Buy):
            self.have_buy = True

            sig_info = self.buy()
            pprint(sig_info)

            buy_info = self.buy_info
            print(buy_info)

            if buy_info and util.get_config('strategy', 'is_mail'):
                util.send_mail('m_b', buy_info)

            logger.info("strategy completed")

        return self.have_buy


if __name__ == '__main__':
    pass

