import datetime
from time import sleep
from urllib.parse import urlparse, urljoin, urlencode
import urllib
from urllib.request import urlopen
import re
from urllib import robotparser
import lxml.html
import requests, sqlite3
from win32.win32crypt import CryptUnprotectData
import os
import pytesseract
from io import BytesIO
import base64
import time
from PIL import Image
from storage import RedisProxy, RedisCookie
import json
from pyquery import PyQuery as pq
import aiohttp
import asyncio
from aiohttp.client_exceptions import ClientError, ClientConnectionError
from flask import Flask, g
from multiprocessing import Process
from selenium import webdriver
import random

from settings import POOL_UPPER__THRESHOLD, VALID_STATUS_CODE, TEST_URL, BATCH_TEST_SIZE, \
TEST_CYCLE,\
GET_CYCLE,\
TEST_ENABLED,\
GET_ENABLED,\
API_ENABLED,\
API_IP,\
API_PORT,\
GENERATOR_MAP,\
TESTER_MAP,\
COOKIEGENERATOR_ENABLED,\
COOKIETESTER_ENABLED

class Throttle:
    """
    较短间隔时间连续获取某个网站的信息可能会被禁IP，所以限时访问
    """
    def __init__(self, delay):
        self.delay = delay
        self.domain = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domain.get(domain)

        if self.delay > 0 and last_accessed is not None:
            # 访问时间间隔如果小于指定间隔，则取差值进行休眠
            sleep_secs = self.delay - (datetime.datetime.now() - self.domain[domain]).seconds
            if sleep_secs > 0:
                sleep(sleep_secs)
        self.domain[domain] = datetime.datetime.now()

def get_links(html):
    """
    获取html页面中的所有链接
    """
    links_regex = re.compile(r'<a[^>]+href=["\'](.*?)["\']')
    return links_regex.findall(html)


class Can_fetch():
    """
    检查是否可以访问网站
    """
    def __init__(self, url, agent):
        self.rp = robotparser.RobotFileParser()
        self.url = url
        self.robotTxt = urljoin(url, '/robots.txt')
        self.agent = agent

    def can_fetch(self):
        self.rp.set_url(self.robotTxt)
        self.rp.read()
        return self.rp.can_fetch(self.agent, self.url)

def getFormData(html):
    """
    获取需要表单元素
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data

class AuthenFail(Exception):
    """
    登录失败
    """

class CaptchaError(Exception):
    """
    通过请求API获取验证码失败
    """
    
def getCookieFromChrome(host_key):
    """
    根据域名host_key获取谷歌浏览器cookie数据
    """
    cookiepath = os.environ['LOCALAPPDATA'] +r'\Google\Chrome\User Data\Default\Cookies'
    print(cookiepath)
    # Chrome的cookie存储在sqlite数据库中，name:value 其中的
    # value值是经过CryptprotectData加密的
    # 需要使用windows的CryptUnprotectData解密函数进行解密
    with sqlite3.connect(cookiepath) as conn:
        cursor = conn.cursor()
        querySql = 'select host_key, name, encrypted_value from cookies where host_key="{}"'.format(host_key)
        cookieData = {name:CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value in cursor.execute(querySql).fetchall()}
        print(cookieData)
        return cookieData

def get_captcha(img_ori):
    """
    提取图片认证码,针对文字辨识度较高的图片有效
    确保安装了tesseract并配置了正确的环境变量
    """
    # 保存灰度图像
    file_like = BytesIO(img_ori)
    img = Image.open(file_like)
    gray = img.convert('L')
    # (0~1：由白至黑过度)，对每一个像素阈值化处理，只保留纯黑纯白部分
    # 这样背景与前景就能很好地区分开来
    bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    bw.save()
    captcha = pytesseract.image_to_string(bw)

    return captcha

class CaptChaAPI:
    """
    根据已知的apikey和本地的验证码图像数据发送请求到9kw，获取返回的captchaid，根据captchaid
    请求9kw，获取验证码处理的结果文字
    9kw其实是由各个用户进行人工检查验证码的
    如果发送相同的图像数据，9kw服务器会从缓存读取数据
    可以帮别人验证验证码，获取积分
    注：9kw帐户:176..@qq.com/6ZJ34BHNXT8P6XT
    """

    def __init__(self, api_key=None, timeout=60):
        self.api_key = api_key if api_key is not None else 'X8BOZF05VI5GZGCGH1'
        self.timeout = timeout
        self.url = 'https://www.9kw.eu/index.cgi'

    # 获取9kw的API处理后的图片验证码的结果
    def get_captcha(self, img):
        file_like = BytesIO(img)
        imgdata = Image.open(file_like)
        # 数据编码为base64
        byte_buffer = BytesIO()
        imgdata.save(byte_buffer, format='PNG')
        data = byte_buffer.getvalue()
        base64Data = base64.b64encode(data)

        captcha_id = self.send(base64Data)
        start_time = time.time()

        while time.time() < start_time + self.timeout:
            try:
                text = self.get(captcha_id)
            except CaptchaError:
                pass
            else:
                if text != 'NO DATA':
                    if text == 'ERROR NO USER':
                        raise CaptchaError('Error: 当前无用户在处理验证码')
                    else:
                        print('验证码请求成功!')
                    return text
            print('正在请求...')
        print('Error: API 超时!')

    def send(self, imgdata):
        print("Submmiting Captcha...")
        data = {
            "apikey": self.api_key,
            "action": "usercaptchaupload",
            "file-upload-01": imgdata,
            "base64": "1",
            "maxtimeout": str(self.timeout),
            # 如果为1表示自己处理，为0让他人处理，不过会消耗积分
            "selfsolve": "0"
        }
        encoded_data = urlencode(data).encode()
        request = urllib.request.Request(self.url, data=encoded_data)
        resp = urlopen(request)
        rls = resp.read().decode()
        self.check(rls)
        return rls

    def get(self, captcha_id):
        data = {
            "apikey": self.api_key,
            "action": "usercaptchacorrectdata",
            "id": captcha_id,
            # 没有得到结果时返回NO DATA
            "info": 1
        }
        encoded_data = urlencode(data)
        resp = urlopen(self.url + '?' + encoded_data)
        rls = resp.read().decode()
        self.check(rls)
        return rls

    def check(self, result):
        # apikey错误
        if re.match(r'00\d\d \w+', result):
            raise CaptchaError('API error:', result)

def getAgent():
    """
    获取随机user-agent
    """
    return random.choice([
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
        ])

# 代理元类
class ProxyMetaclass(type):
    # 参数：1.当前准备创建的类的对象 2.类的名字 3.类继承的父类集合 4.类的方法集合
    def __new__(cls, name, bases, attrs):
        cnt = 0
        attrs['_CrawlFunc_'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['_CrawlFunc_'].append(k)
                cnt += 1
        attrs['_CrawlFuncCount_'] = cnt
        return type.__new__(cls, name, bases, attrs)

class CrawlProxy(object, metaclass=ProxyMetaclass):
    """
    获取代理
    """
    def __init__(self):
        self.header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        }

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('获取代理:', proxy)
            proxies.append(proxy)
        return proxies

    # 获取有代理网站免费代理IP
    def crawl_youdaili(self):
        start_url = 'https://www.youdaili.net/Daili/http/368{:02d}.html'
        urls = [start_url.format(page) for page in range(13, 0, -1)]
        for url in urls:
            print('下载有代理数据:', url)
            html = requests.get(url, headers=self.header).content.decode()
            doc = pq(html)
            rls = doc('.content p')
            for p in rls:
                ipports = p.text_content()
                for ipport in re.findall(r'([\d.:]+)#', ipports):
                    yield ipport

    # 获取快代理网站免费代理IP
    def crawl_kuaidaili(self, page_cnt=20):
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1, page_cnt + 1)]
        for url in urls:
            print('下载块代理数据:', url)
            html = requests.get(url, headers=self.header).content.decode()
            doc = pq(html)
            rls = doc('table tr')
            # 去掉表头
            rls = rls[1:0]
            # tr类型为lxml.html.HtmlElement
            for tr in rls:
                ip = tr.getchildren()[0].text
                port = tr.getchildren()[1].text
                yield ':'.join([ip, port])

class StorageProxy():
    """
    存储代理
    """
    def __init__(self):
        self.redis = RedisProxy()
        self.crawler = CrawlProxy()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER__THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('开始入库--------')
        for callback_label in range(self.crawler._CrawlFuncCount_):
            callback_func = self.crawler._CrawlFunc_[callback_label]
            proxies = self.crawler.get_proxies(callback_func)
            for proxy in proxies:
                self.redis.add(proxy)

class TestProxy(object):
    """
    测试代理
    """
    def __init__(self):
        self.redis = RedisProxy()
    # 异步协程函数，不会导致阻塞
    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode()
                real_proxy = 'http://' + proxy
                print('正在测试:',proxy)
                # 异步请求，get方法类似于reuqests的get方法
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODE:
                        self.redis.add_max(proxy)
                        print('代理可用:', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('响应码不正确，代理可能不可用:', proxy)
            #except (ClientError, ClientConnectionError, TimeoutError, AttributeError):
            except:
                self.redis.decrease(proxy)
                print('代理请求失败:', proxy)
    def run(self):
        print('代理测试器开始运行')
        try:
            proxies = self.redis.all()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                # 同时并发BATCH_TEST_SIZE个协程
                loop.run_until_complete(asyncio.wait(tasks))
                sleep(5)
        except Exception as e:
            print('测试器运行错误:', e.args)

def FlaskWebApiProxy(host, port):
    """
    通过web接口访问代理
    """
    __all__ = ['app']
    app = Flask(__name__)
    
    def get_conn():
        if not hasattr(g, 'redis'):
            g.redis = RedisProxy()
        return g.redis
    
    @app.route('/')
    def index():
        return '<h2>Welcome To Visit The Proxy Pool</h2>'

    @app.route('/random')
    def get_proxy():
        conn = get_conn()
        return conn.random()
    
    @app.route('/count')
    def get_cnt():
        conn = get_conn()
        return str(conn.count())

    app.run(host, port)


class ProxyScheduler():
    """
    调度代理：获取，存储，测试，调用
    """
    def scheduler_test(self, cycle=TEST_CYCLE):
        test = TestProxy()
        while cycle:
            print('测试器开始执行')
            test.run()
            cycle -= 1
            sleep(5)

    def scheduler_get(self, cycle=GET_CYCLE):
        get = StorageProxy()
        while cycle:
            print('抓取器开始执行')
            get.run()
            cycle -= 1
            sleep(5)

    def scheduler_api(self):
        print('代理API开启:',API_IP,API_PORT)
        FlaskWebApiProxy(API_IP, API_PORT)

    def run(self):
        print('代理调度器开始执行')
        if TEST_ENABLED:
            test_process = Process(target=self.scheduler_test)
            test_process.start()

        if GET_ENABLED:
            get_process = Process(target=self.scheduler_get)
            get_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()

def get_proxy():
    """
    随机获取一个可用代理
    """
    proxy_url = 'http://' + API_IP + ":" + str(API_PORT) + '/random'
    try:
        return requests.get(proxy_url).text
    except ConnectionError:
        return None


class CookieGenerator(object):
    """
    cookie生成模块父类, 在数据库先存储站点用户名与密码,之后根据
    用户名与密码登录站点，之后通过webdriver获取到cookie,账户信息
    存储在名为account:website(自定站点名)的hash表中, 根据账户登录浏览器获取
    的cookie存储在名为cookies:website的hash表中
    """
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisCookie('cookies', self.website)
        self.accounts_db = RedisCookie('accounts', self, website)
        self.init_br()

    def __del__(self):
        self.close()

    def init_br(self):
        self.br = webdriver.Chrome()

    def new_cookies(self, username, pwd):
        raise NotImplementedError

    def process_cookies(self, cookies):
        dicts = {}
        for cookie in cookies:
            dicts[cookie['name']] = cookie['value']
        return dicts

    def run(self):
        accounts_usernames = self.accounts_db.username()
        cookies_usernames = self.cookies_db.username()

        for username in accounts_usernames:
            if not username in cookies_usernames:
                pwd = self.accounts_db.get(username)
                print('正在生成cookie:账户 {}, 密码 {}'.format(username, pwd))
                rls = self.new_cookies(username, pwd)
                if rls.get('status') == 1:
                    cookies = self.process_cookies(rls.get('content'))
                    print('成功获取cookie:{}'.format(cookies))
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('成功保存cookie')
                elif rls.get('status') == 2:
                    print('cookie获取失败:{}'.format(rls.get('content')))
                    if self.accounts_db.delete(username):
                        print('删除账户成功')
                else:
                    print('cookie获取失败:{}'.format(rls.get('content')))

    def close(self):
        try:
            print('Closing Browser')
            self.br.close()
            del self.br
        except TypeError:
            print('Browser not opened')

class TestCookie(object):
    """
    cookie检测模块
    """
    def __init__(self, website='default'):
        self.website = website
        self.accounts_db = RedisProxy('accounts', self.website)
        self.cookies_db = RedisProxy('cookies', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookie_groups = self.cookies_db.all()
        for username, cookie in cookie_groups.items():
            self.test(username, cookie)

def FlaskWebApiCookie(host, port):
    """
    # cookie池访问API
    """            
    app = Flask(__name__)
    @app.route('/')
    def index():
        return '<h2>Welcome To Visit The Cookie Pool</h2>'

    def get_conn():
        for website in GENERATOR_MAP:
            if not hasattr(g, website):
                setattr(g, website + '_cookies', eval('RedisCookieCli' + '("cookies", "' + website + '")'))
            return g
    
    @app.route('/<website>/random')
    def random(website):
        g = get_conn()
        cookies = getattr(g, website + '_cookies').random()
        return cookies

    app.run(host, port)

# 调度cookie池模块
class SchedulerCookie(object):
    @staticmethod
    def test_cookie(cycle=5):
        while True:
            print('cookie测试器开始运行')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('cookie测试完成')
                    del tester
                    sleep(cycle)
            except Exception as e:
                print('发生异常:{}'.format(e.args))

    @staticmethod
    def generator_cookie(cycle=1):
        while cycle:
            print('cookie生成器开始运行')
            try:
                for website, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('cookie生成完成')
                    generator.close()
                    sleep(cycle)
            except Exception as e:
                print('发生异常:{}'.format(e.args))

            cycle -= 1

    @staticmethod
    def api():
        print('cookie池API接口开始运行')
        FlaskWebApiCookie(API_IP, API_PORT)
    
    def run(self):
        if API_ENABLED:
            api_process = Process(target=SchedulerCookie.api)
            api_process.start()
        if COOKIEGENERATOR_ENABLED:
            generator_process = Process(target=SchedulerCookie.generator_cookie)
            generator_process.start()
        if COOKIETESTER_ENABLED:
            tester_process = Process(target=SchedulerCookie.test_cookie)
            tester_process.start()