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




if  __name__ == '__main__':
    url = 'https://www.baidu.com/s?wd=风景&pn=1'
    br = WebDriver()
    rls = br.getHtml(url)
    tree = lxml.html.fromstring(rls)
    data = tree.xpath(r'//div[contains(@id, "content_left")]/div[contains(@class, "c-container")]')
    print(data)
    #print(dir(data[0]))
    for d in data:
        links = d.xpath('//h3/a')
        for link in links:
            print(link.text_content())
            print(link.get('href'))

        summarys = tree.cssselect('div.c-abstract')
        for summary in summarys:
            print(summary.text_content())

            
