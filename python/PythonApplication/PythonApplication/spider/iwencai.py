from selenium import webdriver
import json
import os
from time import sleep
import numpy as np
import sys
import datetime

toolDir = os.path.dirname(os.path.dirname(__file__))
RuleDir = os.path.join(toolDir, 'db')
sys.path.append(RuleDir)

from mysql import MysqlClient

configPath = os.path.dirname(__file__)
file = os.path.join(configPath, 'setting.json')
with open(file, 'r') as f:
    jsonStr = f.read()
    jsonStr = jsonStr.replace('\\', '\\\\')
    config = json.loads(jsonStr)

config_chrome = config['chrome']

class WebDriver(object):
    """
    iwencai今日涨停概念股数据
    """
    def __init__(self, browser=None, brpath=None, option='--headless', url=None):
        self.chrome_options = webdriver.ChromeOptions()

        for arg in config_chrome['argument']:
            self.chrome_options.add_argument(arg)

        self.executable_path = config_chrome['webdriverpath']

        self.br = webdriver.Chrome(executable_path = self.executable_path, chrome_options=self.chrome_options)
        self.br.get(url)

        self.db = None
        self.initDB()
        np.set_printoptions(suppress=True)

    def __del__(self):
        self.db.commit()
        self.br.close()

    def getPageNum(self):
        """
        页面数量
        """
        e = self.br.find_element_by_class_name('total')
        self.br.implicitly_wait(30)
        pageNum = e.text

        return (int(pageNum[1:len(pageNum)-1]))

    def geteachPage(self):
        """
        每页数据条数
        """
        e = self.br.find_elements_by_css_selector('.static_con td[colnum="0"]')
        self.br.implicitly_wait(30)
        return len(e)

    def filterData(self, qtArray):
        """
        过滤数据
        """
        qtArray = qtArray[1:,:]
        qtArray = qtArray.T
        qtArray = np.delete(qtArray, 8, axis=1)

        def deal(array):
            array[5] = array[5].replace('更多', '')
            array[5] = array[5].replace('\n', '')
            array[12] = array[12].replace(',', '')
            array[17] = array[17].replace(',', '')
            array[18] = array[18].replace('\n', '')
            return array

        # 转换数据类型
        t = np.dtype([('symbol', np.str_, 7), ('name', np.str_, 20), ('curpri', np.float16), \
         ('quotechange', np.float16), ('dailylimit', np.str_, 5), ('concept', np.str_, 100), \
         ('sczysj', np.str_, 13), ('zzztsj', np.str_, 13), ('lxztts', 'i4'), \
         ('ztyylb', np.str_, 50), ('ztfdl', np.str_, 20), ('ztfde', np.str_, 20), \
         ('ztfcb', np.float16), ('ztflb', np.float16), ('ztkbcs', 'i4'), \
         ('agltsz', np.str_, 20), ('ssgnsl', 'i4'), ('ssts', 'i4'), \
         ('ssthshy', np.str_, 100)])

        qtArray = list(map(deal, qtArray))
        qtArray = list(map(tuple, qtArray))

        qtArray = np.array(qtArray, dtype=t)

        return qtArray

    def initDB(self):
        """
        初始化数据库
        """
        db_config = config['database']['localhost']
        db_Param = {
            "host": db_config['host'],
            "port": db_config['port'],
            "user": db_config['user'],
            "password": db_config['password'],
            "database": db_config['db']
        }

        self.db = MysqlClient(**db_Param)

        delSql = 'delete from quotation_iwencai_ztgn where date1 = "{}"'.format(str(datetime.datetime.today().date()))
        self.db.execute(delSql)

    def dataToDB(self, array):
        """
        数据入库
        """
        insSql = '''insert into quotation_iwencai_ztgn(date1, symbol, name, curpri, quotachange, dailylimit, concept, sczysj, zzztsj, 
                 lxztts, ztyylb, ztfdl, ztfde, ztfcb, ztflb, ztkbcs, agltsz, ssgnsl, ssts, ssthshy)
                 VALUES("''' + str(datetime.datetime.today().date()) + '''", "{}", "{}",  {},  {}, "{}", "{}", "{}", "{}", {}, 
                "{}", "{}", "{}", {}, {},  {}, "{}", {}, {}, "{}");'''
        for qt in array:
            self.db.execute(insSql.format(*qt))

    def run(self):
        cssSellist = []
        cssSellist.extend(['.static_con td[colnum="{}"]'.format(num) for num in range(2)])
        cssSellist.extend(['.scroll_tbody_con td[colnum="{}"]'.format(num) for num in range(2, 20)])

        eachPage = self.geteachPage()
        qtArray = []
        qtArray = np.empty([1, eachPage])

        # 第一页数据
        for sel in cssSellist:
            tmp = []
            et = self.br.find_elements_by_css_selector(sel)
            self.br.implicitly_wait(30)
            for e in et:
                tmp.append(e.text)

            qtArray = np.append(qtArray, [tmp], axis=0)

        qtArray = self.filterData(qtArray)
        self.dataToDB(qtArray)

        pageNum = self.getPageNum()
            
        # 剩余页数据
        for _ in range(pageNum - 1):
            e = self.br.find_element_by_class_name('next')
            self.br.implicitly_wait(30)
            e.click()
            sleep(2)

            eachPage = self.geteachPage()
            qtArray = np.empty([1, eachPage])

            for sel in cssSellist:
                tmp = []
                et = self.br.find_elements_by_css_selector(sel)
                self.br.implicitly_wait(30)
                for e in et:
                    tmp.append(e.text)

                qtArray = np.append(qtArray, [tmp], axis=0)

            qtArray = self.filterData(qtArray)
            self.dataToDB(qtArray)

            
if __name__ == '__main__':
    url = """http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=index_rewrite&selfsectsn=
             &querytype=stock&searchfilter=&tid=stockpick&w=%E6%B6%A8%E5%81%9C%2C%E6%A6%82%E5%BF%B5"""
    web = WebDriver(url=url)
    web.run()