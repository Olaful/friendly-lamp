from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from time import sleep
import numpy as np

class WebDriver(object):
    """
    webdriver能使用响应浏览器的驱动打开浏览器
    """
    def __init__(self, browser=None, brpath=None, option='--headless', url=None):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错

        self.chrome_options.add_argument('window-size=1366x768') #指定浏览器分辨率
        self.chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        self.chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        self.chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
        # self.chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        self.chrome_options.binary_location = brpath if brpath else r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #手动指定使用的浏览器位置

        self.br = webdriver.Chrome(chrome_options=self.chrome_options)
        self.br.get(url)
        self.wait = WebDriverWait(self.br, 10)
        self.pagenum = self.getInitInfo()

    def __del__(self):
        self.br.close()

    def getInitInfo(self):
        e = self.br.find_element_by_class_name('total')
        self.br.implicitly_wait(30)
        pageNum = e.text
        return int(pageNum[1:len(pageNum)-1])

    def run(self):
        for _ in range(1):
            code = []
            curpri = []
            e = self.br.find_element_by_class_name('next')
            self.br.implicitly_wait(30)
            e.click()
            sleep(2)

            # 股票代码，股票简称
            en = self.br.find_elements_by_css_selector('.static_con td[colnum="0"]')
            self.br.implicitly_wait(5)
            for ee in en:
                code.append(ee.text)
            #现价
            en = self.br.find_elements_by_css_selector('.scroll_tbody_con td[colnum="2"]')
            self.br.implicitly_wait(5)
            for ee in en:
                curpri.append(ee.text)
            
            # 涨跌幅.....

            # 连接
            qt = np.array([code, curpri])
            for i in range(len(qt[0])):
                print(qt[:,i])
            

        


if __name__ == '__main__':
    url = """http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=index_rewrite&selfsectsn=
             &querytype=stock&searchfilter=&tid=stockpick&w=%E6%B6%A8%E5%81%9C%2C%E6%A6%82%E5%BF%B5"""
    web = WebDriver(url=url)
    web.run()