import json
import abc
import datetime
from invest import (util, common)
from invest.stk_data import get_real_time_quo

logger = util.get_logger()


class StrategyBase(abc.ABC):
    def __init__(self):
        self._buy_reason = []
        self._sell_reason = []
        self._check_table()

    @classmethod
    @abc.abstractmethod
    def name(cls):
        return ''

    @property
    @abc.abstractmethod
    def cfg_name(self):
        return ''

    @property
    @abc.abstractmethod
    def pools(self):
        return []

    @property
    def buy_reason(self):
        return self._buy_reason

    @property
    def sell_reason(self):
        return self._sell_reason

    @property
    def symbol_pools(self):
        symbol_list = []
        for pool in self.pools:
            symbols = common.get_stock_pool(pool)
            symbol_info = list(zip([pool] * len(symbols), symbols))
            symbol_list.extend(symbol_info)

        return symbol_list

    @abc.abstractmethod
    def check_config(self):
        pass

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

    def record_sell_info(self, symbol, sell_type, **remark):
        """
        record the info of sell
        """
        if len(self._sell_reason) > util.get_config(self.cfg_name, 'max_pos'):
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
        if len(self._buy_reason) > util.get_config(self.cfg_name, 'max_pos'):
            self._buy_reason.clear()

        rmk = {}
        rmk['symbol'] = symbol
        rmk['pool'] = pool
        rmk.update(remark)
        j_remark = json.dumps(rmk)
        j_remark = j_remark.replace('"', '').replace('{', '').replace('}', '')

        self._buy_reason.append(j_remark)

    def stop_loss(self, pos, loss):
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

        if pos_rtn <= loss:
            self.record_sell_info(pos['symbol'], 'stop loss', avg_price=pos['avgprice'], last_price=round(last_price, 2))
            return True

        return False

    def take_profit(self, pos, profit):
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

        if pos_rtn >= profit:
            self.record_sell_info(pos['symbol'], 'take profit', avg_price=pos['avgprice'], last_price=round(last_price, 2))
            return True

        return False

    def max_hold_day_sell(self, pos, max_hold_day):
        """
        sell if reach max hold day
        """
        addpos_date = str(pos['lastaddpostime'])[:10]
        today = str(datetime.datetime.today().date())

        hold_day = util.traday_diff(addpos_date, today)

        logger.info(f"{pos['symbol']} hold day: {hold_day}")

        if hold_day >= max_hold_day:
            self.record_sell_info(pos['symbol'], 'max hold day', addpos_date=addpos_date, hold_day=hold_day)
            return True

        return False