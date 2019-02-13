import socket
from aide import Throttle, get_links, getFormData, AuthenFail
from urllib.parse import urlparse, quote
import random
import urllib
from urllib.request import build_opener, ProxyHandler
import re
from threading import Thread
import os
from time import sleep
from settings import TIME_SLEEP
from storage import MongoQueue
import multiprocessing
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebView
import time
from selenium import webdriver
import lxml.html
from urllib.parse import urlencode
import http.cookiejar
import ssl
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler
import mechanicalsoup
import requests

class Downloader:
    """
    downloadler类，先读取缓存的内容，没有再从网络上获取后再写入缓存
    ps: 避免爬取被禁方法: 1.设置UA;2.设置proxy代理;3.下载之间延迟;4.禁止cookie
    5.如果可能，访问cache获取;6.分布式下载
    """
    def __init__(self, delay=1, user_agent='wswp', timeout=1000, proxies=None, num_retries=3, get_way='normal', cache=None):
        # 对整个socket设置连接的超时时间, urlopen的read会调用socket接口
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache
        self.timeout = timeout
        self.way = get_way

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                try:
                    if self.num_retries > 0 and 500 <= result['code'] < 600:
                        result = None
                except TypeError:
                    pass
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data = None):
        print('Downloading:',url, headers, proxy)
        request = urllib.request.Request(url, data, headers = headers)
        opener = build_opener()

        if proxy:
            proxy_params = {urlparse(url).scheme: urlparse(url).scheme + "://" + proxy + '/'}
            opener.add_handler(ProxyHandler(proxy_params))

        try:
            html = None
            code = None
            if self.way != 'requests':
                resp = opener.open(request, timeout=self.timeout)
                html = resp.read()
                code = resp.code
            else:
                resp = requests.get(url, proxies=proxy_params, headers = headers)
                html = resp.content
                code = resp.status_code
        except urllib.request.URLError as e:
            print('Download error:',e.reason)

            if hasattr(e, 'code') > 0:
                print(e.code)
                if num_retries > 0 and 500 <= e.code < 600:
                    code = e.code
                    self.download(url, headers, proxy, num_retries - 1, data = None)
                else:
                    code =None
        except Exception:
            ''

        return {'html': html, 'code': code}

def link_crawler(seed_url, link_regex, delay=3, timeout=1000, max_urls=10, max_depth=3, user_agent='wswp', proxies=None, num_retries=1, scrape_callback = None, cache=None):
    """
    max_depth：最多爬取多少网页链接，scrape_callback自定义处理函数，如把
    网站数据保存至本地文件
    """
    craw_queue = [seed_url]
    #seen = set(craw_queue)
    seen = {seed_url:0}
    #throttle = Throttle(0)
    # 最大爬取网页数目
    num_urls = 0
    downloader = Downloader(delay=delay, user_agent=user_agent, timeout=timeout, proxies=proxies, num_retries=num_retries, cache=cache)

    while craw_queue:
        url = craw_queue.pop()

        #throttle.wait(url)

        html = downloader(url)

        if html is not None: html = html.decode('utf-8')

        if scrape_callback:
            scrape_callback(url, html)

        depth = seen[url]
        # 判断是否爬取到了最大深度，有些网站其中的链接会无限循环，
        # 导致爬取出现死循环
        if depth != max_depth:
            for link in get_links(html):
                # 只获取特定网页的链接
                if re.search(link_regex, link):
                    # 获取网页绝对路径，link中可能含有/page/类似的相对路径
                    link = urljoin(url, link)
                    # 已经抓取过的不再抓取，也可以避免在互相有各自连接的两个页面之间反复跳跃
                    if link not in seen:
                        seen[link] = depth + 1
                        # 只抓取同一domain的链接
                        if urlparse(seed_url).netloc == urlparse(link).netloc:
                            craw_queue.append(link)
        num_urls += 1
        if num_urls == max_urls:
            break

def thread_link_crawler(seed_url, delay=3, timeout=1000, user_agent='wswp', max_threads=5, proxies=None, num_retries=1, scrape_callback=None, cache=None):
    """
    多线程同时爬取网站链接信息，爬取队列从mongodb中获取
    """
    print('pid is : {}'.format(os.getpid()))
    craw_queue = MongoQueue()
    craw_queue.clear()
    # 存入mongodb中
    craw_queue.push(seed_url)
    downloader = Downloader(delay=delay, user_agent=user_agent, timeout=timeout, proxies=proxies, num_retries=num_retries, cache=cache)

    def process_queue():
        # 首先从从网址大全中获取所有url,依次存入mongodb中，再逐个url抓取
        while True:
            try:
                url = craw_queue.pop()
            except KeyError:
                break
            else:
                html = downloader(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print('Error in Callback for {}:{}'.format(url, e))
                    else:
                        for link in links:
                            craw_queue.push(link)
            craw_queue.complete(url)

    threads = []
    # craw_queue用于判断时会调用其特殊方法__bool__
    while threads or craw_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < max_threads and craw_queue:
            # 将爬取函数放在线程中执行
            thread = Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
            # 等待上一个进程开启完后再开启下一个进程
            sleep(TIME_SLEEP)

def process_crawler(args, **kwargs):
    """
    多进程爬取网站链接
    cpu核数决定能开多少个相同的进程
    """
    nums_cpus = multiprocessing.cpu_count()
    print('Starting {} processes'.format(nums_cpus))
    processes = []
    for _ in range(nums_cpus):
        p = multiprocessing.Process(target=thread_link_crawler, args=[args], kwargs=kwargs)
        # 开启进程
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


class BrowserRender(QWebView):
    """
    QWebKit实现的浏览器，渲染动态页面
    """
    def __init__(self, show=True):
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


class WebDriver(object):
    """
    webdriver能使用响应浏览器的驱动打开浏览器
    """
    def __init__(self, browser=None, brpath=None, option='--headless'):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')#解决DevToolsActivePort文件不存在的报错

        self.chrome_options.add_argument('window-size=1366x768') #指定浏览器分辨率
        self.chrome_options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
        self.chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
        self.chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
        self.chrome_options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        self.chrome_options.binary_location = brpath if brpath else r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" #手动指定使用的浏览器位置

        self.br = webdriver.Chrome(chrome_options=self.chrome_options)

    def __del__(self):
        ''
        # self.br.close()

    def getHtmlByXpath(self, url, xpath):
        self.br.get(url)
        self.br.implicitly_wait(30)
        self.br.find_element_by_xpath(xpath)
        return self.br.page_source

    def run_query(self, key_word):
        url = 'https://www.baidu.com/s?wd={}&pn=1'.format(key_word)
        rls = self.getHtmlByXpath(url, '//div[contains(@class, "c-container")]')
        self.br.close()

        tree = lxml.html.fromstring(rls)
        data = tree.xpath(r'//div[contains(@id, "content_left")]/div[contains(@class, "c-container")]/h3[contains(@class, "t")]/a')
        
        result = []
        for d in data:
            result.append({'title': d.text_content(), 'link': d.get('href'), 'summary': ''})

        return result

class loginAndGetHtml(object):
    """
    访问某些需要登录的界面，kwargs收集用户登录信息
    """
    def __init__(self, login_url, **kwargs):
        self.login_url = login_url
        self.kw = kwargs

    def getHtml(self, url):
        cj = http.cookiejar.CookieJar()

        # 如果访问https页面，可能会进行ssl认证，这时可以手动取消认证
        if re.match(r'https', url):
            cxt = ssl._create_unverified_context()
            opener = build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPSHandler(context=cxt))
        else:
            opener = build_opener(urllib.request.HTTPCookieProcessor(cj))

        loging_html = opener.open(self.login_url).read()
        data = getFormData(loging_html)

        # 填充表单数据
        for items in self.kw.items():
            data[items[0]] = items[1]

        encode_data = urlencode(data).encode(encoding='utf-8')
        request = urllib.request.Request(url, data=encode_data, headers = {'User-agent': 'wswp'})
        response = opener.open(request)

        if re.search(r'/login', response.geturl):
            raise AuthenFail('登录认证失败')
        
        request = urllib.request.Request(url, data=encode_data, headers = {'User-agent': 'wswp'})
        html = opener.open(request).read()

        return html

class MechLogin(object):
    """
    使用mechanize获取表单内容自动登录
    """
    def __init__(self, login_url, **kwargs):
        self.kw = kwargs
        self.login_url = login_url
        self.browser = mechanicalsoup.StatefulBrowser(soup_config={'features': 'lxml'})

    def __del__(self):
        self.browser.close()

    def getHtml(self, url):
        self.browser.open(self.login_url)
        # nr=0选择匹配到的第一个form
        self.browser.select_form(nr=0)

        for items in self.kw.items():
            self.browser[items[0]] = items[1]
        # 提交所选择的表单的内容
        self.browser.submit_selected()

        if re.search(r'/login', self.browser.get_url()):
            raise AuthenFail('登录认证失败')

        self.browser.open(url)
        html = self.browser.get_current_page()
        return html


class RenderBySplash():
    """
    通过splash返回渲染后的页面,需要开启splash服务
    """
    def __init__(self, splash_url, url):
        self.splash_url = splash_url if splash_url \
            else 'http://192.168.99.100:8050/render.html'
        self.url = url
        self.real_url = self.splash_url + self.url

    def getHtml(self):
        resp = requests.get(self.real_url)
        return resp.text