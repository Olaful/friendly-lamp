import util
from strategy_base import StrategyBase

logger = util.get_logger()


class StratgyTurn(StrategyBase):
    def __init__(self):
        pass

    def check_config(self):
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