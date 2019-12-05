# -*- coding: utf-8 -*-

import unittest
from other import ut

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'], 'no equal')
        # check if raise specified exception
        with self.assertRaises(TypeError) as cm:
            s.split(2)

        exp = cm
        # self.assertEqual(exp.error_code, 3)


class TestCaseA(unittest.TestCase):
    # init some info, if run error, subclass runTest method will not run
    # run before every testcase
    def setUp(self) -> None:
        self.name = 'Mike'

    # end work
    def tearDown(self) -> None:
        self.name = ''

    # compare with setUp, only run once
    @classmethod
    def setUpClass(cls) -> None:
        ''

    @classmethod
    def tearDownClass(cls) -> None:
        ''

# implement A
class TestCaseB(TestCaseA):
    # default test method
    def runTest(self):
        # can use basic class attr
        self.assertEqual(self.name, 'Mike')

class TestCaseC(TestCaseA):
    def runTest(self):
        self.assertEqual(self.name, 'Jake')

    # if define, will only run this method, will not run runTest
    # def test_name(self):
    #     self.assertEqual(self.name, 'Mike')

class TestCaseD(unittest.TestCase):
    def setUp(self) -> None:
        self.name = 'Mike'

    def tearDown(self) -> None:
        self.name = ''

    def test_name1(self):
        self.assertEqual(self.name, 'Mike')

        # if Fail, will continue to exe next assert
        # only one subTest to one assert
        with self.subTest():
            self.assertEqual(self.name, 'MIke')

    def test_name2(self):
        # self define failure msg, will cover the msg of assert
        self.fail(msg='my fail msg')
        self.assertEqual(self.name, 'Jake')

    def test_even(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)

def testFunc():
    assert 1 == 1

class TestCaseE(unittest.TestCase):
    @unittest.skip('test1 skipping')
    def test_1(self):
        self.fail('test fail')

    @unittest.skipIf(1 > 2, 'skip according to contation')
    def test_2(self):
        self.assertEqual('apple', 'banana')

    @unittest.skipUnless(1==1, 'test 3')
    def test_3(self):
        self.assertEqual('apple', 'apple')

    @unittest.expectedFailure
    def test_4(self):
        self.assertEqual(1, 2, 'broken')

# class can also skip
@unittest.skip('skip F')
class TestCaseF(unittest.TestCase):
        def test_1(self):
            ''

class TestCaseG(unittest.TestCase):
    def test_1(self):
        self.assertEqual(1, 1)

    def test_2(self):
        self.assertNotEqual(1, 1)

    def test_3(self):
        self.assertTrue(1)

    def test_4(self):
        self.assertFalse(1)

    def test_5(self):
        self.assertIs(1, 1)

    def test_6(self):
        self.assertIsNot(1, 1)

    def test_7(self):
        self.assertIsNone(1)

    def test_8(self):
        self.assertIsNotNone(1)

    def test_9(self):
        self.assertIn(1, [1])

    def test_10(self):
        self.assertNotIn(1, [1])

    def test_11(self):
        self.assertIsInstance(1, int)

    def test_12(self):
        self.assertNotIsInstance(1, int)

    def test_13(self):
        self.assertRaisesRegexp(ValueError, "hello .*XYZ'$", int, 'XYZ')

    def test_14(self):
        self.assertGreater(1, 2)

    def test_15(self):
        self.assertGreaterEqual(1, 2)

    def test_16(self):
        self.assertLess(1, 2)

    def test_17(self):
        self.assertLessEqual(1, 2)

    def test_18(self):
        self.assertRegexpMatches('ABC', 'A*')

    def test_19(self):
        self.assertNotRegexpMatches('ABC', 'C')

    def test_21(self):
        self.assertDictContainsSubset({1: 1, 3:3}, {1: 1})

class TestCaseH(unittest.TestCase):
    def clear_1(self, p):
        print('enter clean 1', p)
    def clear_2(self, p):
        print('enter clean 2', p)

    def test_1(self):
        # self define failure msg, will cover the msg of assert
        # and force to fail
        # self.fail(msg='my fail msg')
        self.longMessage = True
        self.assertEqual(1, 1, 'broken')

    def test_2(self):
        ''
        # raise self.failureException(ValueError)

    @unittest.skip('1')
    def test_3(self):
        # length of failure msg
        self.maxDiff = 2
        with self.subTest():
            self.assertMultiLineEqual('hello', 'world')

    def test_4(self):
        # test amount
        tc = self.countTestCases()
        print(tc)
        # default test result
        dt = self.defaultTestResult()
        print(dt.failures)
        # self id
        id = self.id()
        print(id)
        # desc info of testcase
        sd = self.shortDescription()
        print(sd)

        ''
    def test_5(self):
        ''
        # if setUp fail, tearDown will not run, but addCleanup will run
        # if exist more than one func, will exe accord LIFO
        self.addCleanup(self.clear_1, 'hello')
        self.addCleanup(self.clear_2, 'world')

        # exe func added by addClenup
        self.doCleanups()

    def mytest_1(self):
        ''
        self.assertEqual(1, 1)

def sort_test(x, y):
    ''
    return x > y

def main():
    # load Test class to run
    # each method result will display on the screen
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCaseE)
    # return test result
    test_rls = unittest.TextTestRunner(verbosity=2).run(suite)
    # with open(r'C:\Users\vado\Desktop\testcaserls.txt', 'w') as f:
    #     test_rls = unittest.TextTestRunner(verbosity=2, stream=f).run(suite)
    # error msg before testcase
    # test_rls.buffer = True
    # fisrt error will call stop() to interrupt
    # test_rls.failfast = True
    #
    # test_rls.shouldStop = True
    # test_rls.tb_locals = True
    # # True if all testcase pass
    # sc = test_rls.wasSuccessful()
    # print(test_rls.errors)
    # print(test_rls.failures)

    # add test method to suite
    # testDSuit = unittest.TestSuite()
    # testDSuit.addTest(TestCaseD('test_name1'))
    # unittest.TextTestRunner(verbosity=2).run(testDSuit)


    # test method set
    # tests = ['test_name1', 'test_name2']
    # testDSuit = unittest.TestSuite(map(TestCaseD, tests))
    # unittest.TextTestRunner(verbosity=2).run(testDSuit)

    # add testcase from multiple module
    # suite1 = ut.TestCaseB()
    # suite2 = ut.TestCaseC()
    # alltests = unittest.TestSuite([suite1, suite2])
    # unittest.TextTestRunner(verbosity=2).run(alltests)

    # add normal func to unittest sys, but the func should
    # be contain assert statement
    # testcase = unittest.FunctionTestCase(testFunc)
    # unittest.TextTestRunner(verbosity=2).run(testcase)

    # load class from module
    # suite = unittest.TestLoader().loadTestsFromModule(other)
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # discover testcase in the dir
    # discover = unittest.defaultTestLoader.discover('other', pattern='u*.py')
    # unittest.TextTestRunner(verbosity=2).run(discover)

    # testLoader define testcase rule
    # loader = unittest.TestLoader()
    # # self define testcase prefix
    # loader.testMethodPrefix = 'mytest'
    # loader.sortTestMethodsUsing = sort_test
    # suite = loader.loadTestsFromTestCase(TestCaseH)
    # # 获取testcase方法名称
    # testCaseName = loader.getTestCaseNames(TestCaseH)
    # print(testCaseName)
    # unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    # verbosity=2 will print more detail info
    # unittest.main(verbosity=2)
    main()