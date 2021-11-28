from invest import common
from invest import util
import time
import quotool
from pprint import pprint
from invest.strategy_base import StrategyBase
from .types import ExeAction
from .stk_data import get_real_time_quo, day_bars
from .b_sig import is_rise_in_good_condition as b_sig_is_rise_in_good_condition
from . import s_sig


logger = util.get_logger()


class StrategyTurn(StrategyBase):
    def __init__(self):
        super().__init__()

        util.init_config('strategy_turn', from_db=True)

        self.check_config()

        self.have_buy = False
        self.have_sell = False

        self._download_day_bar()

    @classmethod
    def name(cls):
        return 'turn'

    @property
    def cfg_name(self):
        return 'strategy_turn'

    @property
    def pools(self):
        return util.get_config('strategy_turn', 'pool')

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

    @property
    def buy_info_html(self):
        """
        buy info
        :return:
        """
        p_style = "color: #000001; font-family: 'DrukTextWideBold', " \
                     "'Helvetica Neue', sans-serif; font-size: 16px; " \
                     "font-synthesis: none; font-weight: bold; " \
                     "line-height: 18px; margin: 0; " \
                     "padding: 0; text-transform: uppercase;"
        html = """
        <div>
            <p style="%s">{code}</p>
            <ul>
                <li>pool: {pool}</li>
                <li>nece_score: {nece_score}</li>
                <li>opt_score: {opt_score}</li>
                <li>necessary_cond:<br> 
                {necessary_cond}
                </li>
                <li>optional_cond:<br> 
                {optional_cond}
                </li>
            </ul>
        </div>
        """ % p_style
        div_list = []
        for buy_info in self.buy_reason_dict:
            necessary_cond = '\n'.join([nc+'<br>' for nc in buy_info['necessary_cond'].split('#')])
            optional_cond = '\n'.join([oc + '<br>' for oc in buy_info['optional_cond'].split('#')])
            html_param = {
                'code': buy_info['symbol'],
                'pool': buy_info['pool'],
                'nece_score': buy_info['nece_score'],
                'opt_score': buy_info['opt_score'],
                'necessary_cond': necessary_cond,
                'optional_cond': optional_cond
            }
            div = html.format(**html_param)
            div_list.append(div)

        divs = '\n'.join(div_list)

        return divs

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
    def is_pin_bar(bars):
        """
        if the bar is a pin bar
        :param bar:
        :return:
        """
        if common.is_cross_star(bars[0], open_close_change=0.0025, high_low_change=0.025):
            return True, bars[:1], 'cross_star'
        elif common.is_hang_line(bars[0], mul=1, up_percent=0.009):
            return True, bars[:1], 'hang_line'
        elif common.is_T_line(bars[0], open_close_change=0.0025, high_low_change=0.025, up_percent=0.009):
            return True, bars[:1], 'T_line'
        elif common.is_bullish_swallow(bars[:2], percent=0.002):
            return True, bars[:2], 'bullish_swallow'
        elif common.is_pierce_line(bars[:2], percent=0.009):
            return True, bars[:2], 'pierce_line'
        elif common.is_start_morrow_star(bars[:3], percent=0.002, open_close_change=0.006):
            return True, bars[:3], 'start_morrow_star'
        elif common.is_go_ahead_red_three_soldier(bars[:3]):
            return True, bars[:3], 'go_ahead_red_three_soldier'
        
        return False, [], ''

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
                return True, pos

        return False, 0

    @staticmethod
    def is_in_high_or_low_pos(day_bars, days=2, direction='down'):
        """
        if in high or low position
        """
        ma5_list = common.get_ma_list(day_bars, freq=5, num=days+1+1)
        pre_ma5_list = ma5_list[1:]
        decline_or_gain_days = util.continuous_decline_or_gain(pre_ma5_list, direction)

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
            return True, hig_low_change

        return False, 0.0

    @staticmethod
    def is_pretend_breakthrough_key_pos(bar, key_pos, change=0.009):
        """
        if pretend to breakthrough the key position
        """
        lower_key_pos = [pos for pos in key_pos if pos < bar['close']]
        if not lower_key_pos:
            return False, 0.0

        nearby_lower_key_pos = max(lower_key_pos)

        if bar['close'] < nearby_lower_key_pos:
            return False, 0.0

        key_low_change = nearby_lower_key_pos / bar['low'] - 1

        if key_low_change >= change:
            return True, nearby_lower_key_pos

        return False, 0.0

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
    def is_key_pos_pl_gt_specify_value(price, key_pos: list = None, pl=1.2, change=0.01):
        """
        if the profit-loss ratio gt specify value
        """
        upper_key_pos = [pos for pos in key_pos if pos > price]
        if not upper_key_pos:
            return False, 0.0

        nearby_upper_key_pos = min(upper_key_pos)

        lower_key_pos = [pos for pos in key_pos if pos < price]
        if not lower_key_pos:
            return False, 0.0

        nearby_lower_key_pos = max(lower_key_pos)

        upper_profit = nearby_upper_key_pos * (1 + change) - price
        lower_loss = price - nearby_lower_key_pos * (1 - change)

        pl_ratio = upper_profit / lower_loss

        if pl_ratio >= pl:
            return True, pl_ratio

        return False, 0.0

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
        util.get_config('strategy_turn', 'sell_sig_weight', s) for s in sig})

        self.record_sell_info(pos['symbol'], 'sell signal', **sig_rmk)

        return True

    @staticmethod
    def get_buy_sig_frame():
        buy_sig = {
            'pool': '',
            'symbol': '',
            'necessary_cond': {
                'is_pin_bar': '',
                'is_in_key_pos': 0,
                'is_in_low_pos': 0,
            },
            'nece_score': 0,
            'optional_cond': {
                'is_noticeable_bar': 0,
                'is_pretend_breakthrough_key_pos': 0,
                'is_left_swallow_right_and_change_gt_pre_bar': False,
                'is_key_pos_pl_gt_threshold': 0,
                'is_rise_in_good_condition': False,
            },
            'opt_score': 0
        }

        return buy_sig

    @staticmethod
    def get_key_pos(day_line_bars):
        """
        get the key pos
        """
        parallel_bars = day_line_bars[:util.get_config('strategy_turn', 'parallel_key_pos_bar_num')]
        parallel_key_poss = common.get_parallel_high_low_key_pos(parallel_bars, wind=util.get_config('strategy_turn', 'key_pos_wind'),
                                                            inner_percent=util.get_config('strategy_turn', 'key_pos_wind_inner_change'),
                                                            outer_percent=util.get_config('strategy_turn', 'key_pos_wind_outer_change'),
                                                             turn_num=util.get_config('strategy_turn', 'key_pos_turn_num'))
        gap_bars = day_line_bars[:util.get_config('strategy_turn', 'gap_key_pos_bar_num')]
        gap_key_poss = common.get_gap_key_pos(gap_bars, util.get_config('strategy_turn', 'gap_threshold'))

        key_poss = set(parallel_key_poss + gap_key_poss)
        key_poss = sorted(list(key_poss))

        return key_poss

    def sell(self):
        """
        :return:
        """
        all_pos = common.get_all_pos()

        for pos in all_pos:
            if self.stop_loss(pos, util.get_config('strategy_turn', 'stop_loss')):
                pass
            elif self.take_profit(pos, util.get_config('strategy_turn', 'take_profit')):
                pass
            elif self.max_hold_day_sell(pos, util.get_config('strategy_turn', 'max_hold_day')):
                pass
            elif self.sig_sell(pos):
                pass

    def buy_necess_cond(self, buy_sig, key_poss, day_line_bars, last_day_bar):
        """
        necessary condition
        """
        in_key_pos, key_pos = self.is_in_key_pos(last_day_bar, key_poss,
         change=util.get_config('strategy_turn', 'in_key_pos_change'))
        if in_key_pos:
            buy_sig['necessary_cond']['is_in_key_pos'] = key_pos
            buy_sig['nece_score'] += 1

        if self.is_in_high_or_low_pos(day_line_bars,
         days=util.get_config('strategy_turn', 'in_low_pos_down_day'), direction='down'):
            buy_sig['necessary_cond']['is_in_low_pos'] = True
            buy_sig['nece_score'] += 1

    def buy_option_cond(self, buy_sig, symbol, key_poss, last_day_bar, last_2_day_bars):
        """
        optional condition
        """
        is_noticeable, high_low_change = self.is_noticeable_bar(last_day_bar,
         change=util.get_config('strategy_turn', 'noticeable_bar_change'))
        if is_noticeable:
            buy_sig['optional_cond']['is_noticeable_bar'] = round(high_low_change, 4)
            buy_sig['opt_score'] += 1

        is_pretend_brk, nearby_lower_key_pos = self.is_pretend_breakthrough_key_pos(last_day_bar, key_poss,
         change=util.get_config('strategy_turn', 'pretend_brk_key_pos_change'))
        if is_pretend_brk:
            buy_sig['optional_cond']['is_pretend_breakthrough_key_pos'] = nearby_lower_key_pos
            buy_sig['opt_score'] += 1

        if self.is_left_swallow_right_bar(last_2_day_bars) and self.is_last_change_gt_pre_bar(last_2_day_bars):
            buy_sig['optional_cond']['is_left_swallow_right_and_change_gt_pre_bar'] = True
            buy_sig['opt_score'] += 1

        quo = get_real_time_quo(symbol)
        last_price = float(quo['price'].iloc[0])
        is_gt_pl, pl_ratio = self.is_key_pos_pl_gt_specify_value(last_price, key_poss,
         pl=util.get_config('strategy_turn', 'key_pos_pl'), change=util.get_config('strategy_turn', 'key_pos_pl_change'))
        if is_gt_pl:
            buy_sig['optional_cond']['is_key_pos_pl_gt_threshold'] = round(pl_ratio, 4)
            buy_sig['opt_score'] += 1

        if b_sig_is_rise_in_good_condition(symbol, days=180, step=30, percent=0.6):
            buy_sig['optional_cond']['is_rise_in_good_condition'] = True
            buy_sig['opt_score'] += 1

    def buy(self):
        """
        buy logic
        :return:
        """
        buy_sig_info = []

        for pool, symbol in self.symbol_pools:
            logger.info(f"dealing: {pool} => {symbol}")

            day_line_bars = day_bars(symbol, num=util.get_config('strategy_turn', 'day_bars'))

            buy_sig = self.get_buy_sig_frame()
            buy_sig['pool'] = pool
            buy_sig['symbol'] = symbol

            try:
                is_pin, pin_bars, bar_type = self.is_pin_bar(day_line_bars)
            except Exception as e:
                logger.error(f"{str(e)}", exc_info=True)
                continue

            if is_pin:
                buy_sig['necessary_cond']['is_pin_bar'] = bar_type
                buy_sig['nece_score'] += 1

            last_day_bar = common.merge_bars(pin_bars)
            key_poss = self.get_key_pos(day_line_bars)

            last_day_bar = last_day_bar if last_day_bar else day_line_bars[0]

            self.buy_necess_cond(buy_sig, key_poss, day_line_bars, last_day_bar)

            last_2_day_bars = [last_day_bar, day_line_bars[1]]

            self.buy_option_cond(buy_sig, symbol, key_poss, last_day_bar, last_2_day_bars)

            buy_sig_info.append(buy_sig)
        
        buy_sig_info.sort(key=lambda sig: (sig['nece_score'], sig['opt_score']), reverse=True)

        for b_sig in buy_sig_info:
            if not b_sig['nece_score'] >= 3:
                continue
            if not b_sig['opt_score'] >= 2:
                continue

            sig_rmk = dict()
            sig_rmk['nece_score'] = b_sig['nece_score']
            sig_rmk['opt_score'] = b_sig['opt_score']

            sig_rmk['necessary_cond'] = '#'.join([f"{sig[3:] if sig.startswith('is_') else sig} => {value}"
             for sig, value in b_sig['necessary_cond'].items()])

            sig_rmk['optional_cond'] = '#'.join([f"{sig[3:] if sig.startswith('is_') else sig} => {value}"
             for sig, value in b_sig['optional_cond'].items() if value])

            self.record_buy_info(b_sig['symbol'], b_sig['pool'], **sig_rmk)

        return buy_sig_info

    def run(self):
        """
        run
        :return:
        """
        if self.have_buy:
            return

        if not self.have_sell and self.is_time_exe(ExeAction.Sell) and \
         util.get_config('strategy_turn', 'sell_enable'):
            self.have_sell = True

            self.sell()
            sell_info = '\n'.join(self.sell_reason)
            print(sell_info)

            if sell_info and util.get_config('strategy_turn', 'is_mail'):
                util.send_mail('turn_s', sell_info)

        if not self.have_buy and self.is_time_exe(ExeAction.Buy) and \
         util.get_config('strategy_turn', 'buy_enable'):
            self.have_buy = True

            sig_info = self.buy()
            logger.info(sig_info)
            pprint(sig_info)

            buy_info = self.buy_info
            logger.info(buy_info)
            buy_info_html = self.buy_info_html

            if buy_info and util.get_config('strategy_turn', 'is_mail'):
                util.send_mail('turn_b', buy_info_html)

            logger.info("strategy_turn completed")

        return self.have_buy
