from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import lxml.html

class WebDriver(object):
    def __init__(self, browser=None, option='--headless'):
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument(option)
        # self.chrome_options.set_headless()

        self.chrome_options = Options()

        self.chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错

        self.chrome_options.add_argument('window-size=1366x768') #指定浏览器分辨率
        self.chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        self.chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        self.chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
        self.chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        self.chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #手动指定使用的浏览器位置

    def __del__(self):
        ''
        # self.br.close()

    def getHtml(self, br, url):
        br.get(url)
        br.implicitly_wait(30)
        br.find_element_by_xpath(r'//div[contains(@class, "c-container")]')
        return br.page_source

    def run_query(self, key_word):
        br = webdriver.Chrome(chrome_options=self.chrome_options)
        url = 'https://www.baidu.com/s?wd={}&pn=1'.format(key_word)
        rls = self.getHtml(br, url)
        br.close()

        tree = lxml.html.fromstring(rls)
        data = tree.xpath(r'//div[contains(@id, "content_left")]/div[contains(@class, "c-container")]/h3[contains(@class, "t")]/a')
        
        result = []
        for d in data:
            result.append({'title': d.text_content(), 'link': d.get('href'), 'summary': ''})

        return result


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebView

class BrowserRender(QWebView):
    def __init__(self, show=False):
        self.app = QApplication([])
        QWebView.__init__(self)
        if show:
            self.show()

    def download(self, url, timeout=60):
        loop = QEventLoop()
        timer = QTimer()
        # 设置定时器超时会执行函数
        timer.setSingleShot(True)
        # 定时器超时或者页面加载完成都会触发事件循环退出
        # 如果页面一直没有响应则用定时器终止循环
        timer.timeout.connect(loop.quit)
        self.loadFinished.connect(loop.quit)
        self.load(QUrl(url))
        timer.start(timeout*1000)
        # 一直循环直到loop.quit被调用，之后才继续后面的部分
        loop.exec_()

        # 如果循环结束后，定时器还没有超时，则页面下载完成
        if timer.isActive():
            timer.stop()
            return self.getHtml()
        else:
            print('Request time out:', url)

    def getHtml(self):
        return self.page().mainFrame().toHtml()

    def run_query(self, key_word):
        url = 'https://www.baidu.com/s?wd={}&pn=1'.format(key_word)
        rls = self.download(url)

        tree = lxml.html.fromstring(rls)
        data = tree.xpath(r'//div[contains(@id, "content_left")]/div[contains(@class, "c-container")]/h3[contains(@class, "t")]/a')
        
        result = []
        for d in data:
            result.append({'title': d.text_content(), 'link': d.get('href'), 'summary': ''})

        return result

    def find(self, pattern):
        # css选择器，通过标签名或者class等选择
        return self.page().mainFrame().findAllElements(pattern)

    # 设置html页面元素的值
    def attr(self, pattern, name, value):
        for e in self.find(pattern):
            e.setAttribute(name, value)

    def text(self, pattern, value):
        for e in self.find(pattern):
            e.setPlainText(value)

    # 模拟html页面元素的点击事件，调用相关javascript方法
    def click(self, pattern):
        for e in self.find(pattern):
            e.evaluateJavaScript('this.click()')

    # 在定时内反复查找页面返回的信息，因为ajax调用在规定时间内可能不能及时返回数据
    def wait_load(self, pattern, timeout=60):
        dealine = time.time() + timeout
        while time.time() < dealine:
            # processEvents调用之后就能响应后面的页面事件，app.exec_内部就是调用这个方法
            self.app.processEvents()
            matches = self.find(pattern)
            if matches:
                return matches
        print('Wait load time out')

    # 保持当前窗口
    def keepWindow(self):
        self.app.exec_()

if  __name__ == '__main__':
    br = BrowserRender()
    rls = br.download('https://www.baidu.com/s?wd=电影&pn=1')
            
    tree = lxml.html.fromstring(rls)
    data = tree.xpath(r'//div[contains(@id, "content_left")]/div[contains(@class, "c-container")]/h3[contains(@class, "t")]/a')

    result = []
    for d in data:
        result.append({'title': d.text_content(), 'link': d.get('href'), 'summary': ''})
    
    # br = WebDriver()
    # result = br.run_query('电影')

    print(result)