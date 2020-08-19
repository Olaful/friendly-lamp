import b_sig
import s_sig
import util
import common
from pprint import pprint

logger = None


def _init_config():
    util.init_config('database')
    util.init_config('strategy')


def _init_db():
    util.create_mysql('pool_db')


def _init_logger():
    util.init_logger()


def _init():
    _init_config()
    _init_db()
    _init_logger()


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
    def index_sell_sig(index):
        """
        index sell sig
        :param index:
        :return:
        """
        indicator = util.get_config('strategy', 'index_sell_sig_weight')

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

        return sell_sig, score

    def predict(self, symbol):
        """
        product a predict value
        :param symbol:
        :return:
        """
        buy_sig, b_score = self.buy_sig(symbol)
        sell_sig, s_score = self.sell_sig(symbol)

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

        pprint(sector)

    def run(self):
        """
        run
        :return:
        """
        self.sector_rank()


def main():
    _init()

    global logger
    logger = util.get_logger()

    ms = MyStrategy()
    ms.run()


if __name__ == '__main__':
    main()

