# -*- coding: utf-8 -*-

import unittest
from invest import util, common
from invest.stk_data import day_bars


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
        util.init_config('chrome', from_db=True)
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

    # @unittest.skip('')
    def test_plot(self):
        import invest.plot as plot

        day_line_bar = day_bars('000668')

        key_pos = common.get_parallel_high_low_key_pos(day_line_bar)
        plot.key_line(day_line_bar, key_pos)

    @unittest.skip('')
    def test_captcha(self):
        from PIL import Image
        import hashlib
        from invest.pool_tool.captcha_ident import ChaoJiYingAPI
        img = Image.open(r'E:\picture\iwencai_captcha.png')

        ori_pwd = ''.join([chr(int(w) - 12) for w in util.get_config('chrome', 'chaojiying_upwd').split(',')])
        pwd_md5 = hashlib.md5()
        pwd_md5.update(ori_pwd.encode())
        pwd = pwd_md5.hexdigest()
        cjy = ChaoJiYingAPI(img, 'zinfenkie', pwd, 898312, 1006)
        # rls = cjy.solve()
        test = 1

    @unittest.skip('')
    def test_tmp(self):
        util.send_mail('1', '1')
        test = 1


class TestPool(unittest.TestCase):
    """
    pool test
    """
    from PIL import Image
    from invest.pool_tool.fetch_pool import fetch_pool
    from invest.pool_tool.captcha_ident import CaptCha9KAPI
    # img = Image.open(r'E:\picture\iwencai_captcha.png')
    # cc9k = CaptChaAPI9K(img, api_key='X8BOZF05VI5GZGCGH1')
    # rls = cc9k.solve()

    # fetch_pool()
    test = 1


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFrame)
    rls = unittest.TextTestRunner(verbosity=2).run(suite)
    print('Total TestCase:', rls.testsRun)


if __name__ == '__main__':
    main()

