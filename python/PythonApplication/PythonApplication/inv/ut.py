# -*- coding: utf-8 -*-

import unittest
from invest import util, common


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        初始化程序
        :return:
        """
        util.init_config('database')
        util.create_mysql('test')
        util.init_config('strategy_turn', from_db=True)
        util.init_config('market', from_db=True)
        util.init_config('mail', from_db=True)
        common.init_data()
        util.init_logger()


class TestStrategyTurn(TestBase):
    """
    Turn单元测试
    """
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        from invest.strategy_turn import StrategyTurn

        cls.turn = StrategyTurn()

    def test_tmp(self):
        bar = {'low': 1, 'open': 2, 'close': 2, 'high': 4}
        self.turn.buy()


class TestFrame(TestBase):
    """
    框架测试
    """
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    @unittest.skip('')
    def test_plot(self):
        from invest.stk_data import day_bars
        import invest.plot as plot

        day_line_bar = day_bars('002100')
        day_bar = day_line_bar[0]

        key_pos = common.get_parallel_high_low_key_pos(day_line_bar)
        plot.key_line(day_line_bar, key_pos)

    def test_tmp(self):
        pass


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStrategyTurn)
    rls = unittest.TextTestRunner(verbosity=2).run(suite)
    print('Total TestCase:', rls.testsRun)


if __name__ == '__main__':
    main()

