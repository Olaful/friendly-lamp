from invest import common
from invest import util
import time
from pprint import pprint
import quotool
from invest.strategy_base import StrategyBase
from .types import ExeAction
from .stk_data import get_real_time_quo, day_bars
from .b_sig import is_rise_in_good_condition as b_sig_is_rise_in_good_condition
from . import s_sig


logger = util.get_logger()


class StrategyTurn(StrategyBase):
    def __init__(self):
        super().__init__()

        util.init_config('strategy_turn_turn_turn', from_db=True)

        self.check_config()

        self.have_buy = False
        self.have_sell = False

        self._download_day_bar()

    def check_config(self):
        logger.info('config check')

        assert isinstance(util.get_config('strategy_turn', 'sell_sig_weight'), dict), \
            'sell_sig_weight is not dict'
        assert isinstance(util.get_config('strategy_turn', 'index_sell_sig_weight'), dict), \
            'index_sell_sig_weight is not dict'
        assert util.get_config('strategy_turn', 'index'), \
            'index is null'
        assert util.get_config('strategy_turn', 'pool') and isinstance(util.get_config('strategy_turn', 'pool'), list), \
            'pool is null or is not list'
        assert util.get_config('strategy_turn', 'stop_loss') <= 0, \
            'stop_loss gt 0'
        assert util.get_config('strategy_turn', 'take_profit') >= 0, \
            'take_profit lt 0'
        assert util.get_config('strategy_turn', 'max_hold_day') >= 0, \
            'max_hold_day lt 0'
        assert util.get_config('strategy_turn', 'trailing_loss') <= 0, \
            'trailing_loss gt 0'
        assert util.get_config('strategy_turn', 'before_close_sell') is not None, \
            'before_close_sell is null'
        assert util.get_config('strategy_turn', 'before_close_buy') is not None, \
            'before_close_buy is null'

        logger.info('config check ok')
        
    @property
    def buy_info(self):
        """
        buy info
        :return: 
        """
        buy_info = '\n'.join(self.buy_reason)

        return buy_info

    @staticmethod
    def _download_day_bar():
        """
        download day bar
        """
        all_pos = common.get_all_pos()
        all_symbol = [pos['symbol'] for pos in all_pos]

        pools = util.get_config('strategy_turn', 'pool')
        for pool in pools:
            all_symbol.extend(common.get_stock_pool(pool))

        all_symbol = set(all_symbol)

        for symbol in all_symbol:
            quotool.his_quo(symbol)

        quotool.his_quo(util.get_config('strategy_turn', 'index'), is_index=True)

    @staticmethod
    def is_time_exe(action=None):
        """
        if it is time to execute
        """
        if action == ExeAction.Sell:
            exe_time = common.get_openclose_time()[1] - \
             util.get_config('strategy_turn', 'before_close_sell') * 60
            now = time.time()
            if now >= exe_time:
                logger.info("Time to sell")
                return True
        elif action == ExeAction.Buy:
            exe_time = common.get_openclose_time()[1] - \
             util.get_config('strategy_turn', 'before_close_buy') * 60
            now = time.time()
            if now >= exe_time:
                logger.info("Time to buy")
                return True

        return False

    @staticmethod
    def is_pin_bar(bar):
        """
        if the bar is a pin bar
        :param bar:
        :return:
        """
        if common.is_cross_star(bar, open_close_change=0.0025, high_low_change=0.025):
            return True
        elif common.is_hang_line(bar, mul=1, up_percent=0.009):
            return True
        elif common.is_T_line(bar, open_close_change=0.0025, high_low_change=0.025, up_percent=0.009):
            return True

        return False

    @staticmethod
    def is_in_key_pos(bar, key_pos: list = None, change=0.001):
        """
        if in the key position
        :param bar:
        :param key_pos:
        :param change:
        :return:
        """
        high = bar['high'] * (1 + change)
        low = bar['low'] * (1 - change)

        for pos in key_pos:
            if low <= pos <= high:
                return True

        return False

    @staticmethod
    def is_in_high_or_low_pos(closes, days=2, direction='down'):
        """
        if in high or low position
        """
        decline_or_gain_days = util.continuous_decline_or_gain(closes, direction)

        if decline_or_gain_days >= days:
            return True

        return False

    @staticmethod
    def is_noticeable_bar(bar, change=0.06):
        """
        if it is a noticeable bar
        """
        hig_low_change = bar['high'] / bar['low'] - 1

        if hig_low_change >= change:
            return True

        return False

    @staticmethod
    def is_pretend_breakthrough_key_pos(bar, key_pos, change=0.009):
        """
        if pretend to breakthrough the key position
        """
        if bar['close'] < key_pos:
            return False

        key_low_change = key_pos / bar['low'] - 1

        if key_low_change >= change:
            return True

        return False

    @staticmethod
    def is_left_swallow_right_bar(day_bars):
        """
        if left bar swallow right bar
        """
        if len(day_bars) < 2:
            return False

        last_day_bar = day_bars[0]
        pre_day_bar = day_bars[1]

        if pre_day_bar['high'] >= max(last_day_bar['open'], last_day_bar['close']) \
                and pre_day_bar['low'] <= min(last_day_bar['open'], last_day_bar['close']):
            return True

        return False

    @staticmethod
    def is_last_change_gt_pre_bar(day_bars):
        """
        if change of last bar greater than previous
        """
        if len(day_bars) < 2:
            return False

        last_day_bar = day_bars[0]
        pre_day_bar = day_bars[1]

        last_bar_change = last_day_bar['high'] / last_day_bar['low'] - 1
        pre_bar_change = pre_day_bar['high'] / pre_day_bar['low'] - 1

        if last_bar_change > pre_bar_change:
            return True

        return False

    @staticmethod
    def is_key_pos_pl_gt_specify_value(price, key_pos: list = None, pl=1.5, change=0.01):
        """
        if the profit-loss ratio gt specify value
        """
        upper_key_pos = [pos for pos in key_pos if pos > price]
        if not upper_key_pos:
            return False

        nearby_upper_key_pos = min(upper_key_pos)

        lower_key_pos = [pos for pos in key_pos if pos < price]
        if not lower_key_pos:
            return False

        nearby_lower_key_pos = max(lower_key_pos)

        upper_profit = nearby_upper_key_pos * (1 + change) - price
        lower_loss = price - nearby_lower_key_pos * (1 - change)

        pl_ratio = upper_profit / lower_loss

        if pl_ratio >= pl:
            return True

        return False

    @staticmethod
    def sell_sig(symbol):
        """
        sell sig
        :return:
        """
        indicator = util.get_config('strategy_turn', 'sell_sig_weight')

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

    def sig_sell(self, pos):
        """
        signal to sell
        """
        sell_sig, s_score = self.sell_sig(pos['symbol'])

        if s_score < util.get_config('strategy_turn', 'sell_sig_threshold'):
            return False

        sig = [s_n for s_n, s in sell_sig.items() if s]
        sig_rmk = dict()
        sig_rmk['score'] = round(s_score, 4)
        sig_rmk.update({s[3:] if s.startswith('is_') else s:
        util.get_config('strategy', 'sell_sig_weight', s) for s in sig})

        self.record_sell_info(pos['symbol'], 'sell signal', **sig_rmk)

        return True

    def sell(self):
        """
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
            elif self.sig_sell(pos):
                pass

    def buy(self):
        """
        买入逻辑
        :return:
        """
        pools = util.get_config('strategy_turn', 'pool')

        symbol_list = []
        for pool in pools:
            symbol_list = common.get_stock_pool(pool)

        for symbol in symbol_list:
            day_lin_bars = day_bars(symbol, num=180)
            last_day_bar = day_lin_bars[0]
            day_closes = [bar['close'] for bar in day_lin_bars]

            if not self.is_pin_bar(last_day_bar):
                continue

            key_poss = common.get_parallel_high_low_key_pos(day_lin_bars, wind=30,
                                                            inner_percent=0.01,
                                                            outer_percent=0.02, turn_num=2)
            if not self.is_in_key_pos(last_day_bar, key_poss, change=0.001):
                return False

            if not self.is_in_high_or_low_pos(day_closes, days=2, direction='down'):
                return False

            optional_condition = 0
            last_2_day_bars = day_lin_bars[:2]
            quo = get_real_time_quo(symbol)
            last_price = float(quo['price'].iloc[0])

            if self.is_noticeable_bar(last_day_bar, change=0.06):
                optional_condition += 1
            if self.is_pretend_breakthrough_key_pos(last_day_bar, key_poss, change=0.009):
                optional_condition += 1
            if self.is_left_swallow_right_bar(last_2_day_bars) and self.is_last_change_gt_pre_bar(last_2_day_bars):
                optional_condition += 1
            if self.is_key_pos_pl_gt_specify_value(last_price, key_poss, pl=1.5, change=0.01):
                optional_condition += 1
            if b_sig_is_rise_in_good_condition(symbol, days=180, step=30, percent=0.6):
                optional_condition += 1

            if optional_condition < 2:
                self.record_buy_info(symbol, 'pool', sig=f"2 + {optional_condition}")

    def run(self):
        """
        run
        :return:
        """
        if not self.have_sell and self.is_time_exe(ExeAction.Sell):
            self.have_sell = True

            self.sell()
            sell_info = '\n'.join(self.sell_reason)
            print(sell_info)

            if sell_info and util.get_config('strategy_turn', 'is_mail'):
                util.send_mail('turn_s', sell_info)

        if not self.have_buy and self.is_time_exe(ExeAction.Buy):
            self.have_buy = True

            sig_info = self.buy()
            pprint(sig_info)

            buy_info = self.buy_info
            print(buy_info)

            if buy_info and util.get_config('strategy_turn', 'is_mail'):
                util.send_mail('turn_b', buy_info)

            logger.info("strategy_turn completed")

        return self.have_buy
