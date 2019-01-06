import scrapy

from srppro.items import DmozItem, CSDNItemImg, ProxyItem

from scrapy.loader import ItemLoader

from scrapy import Request

from urllib.parse import urljoin, urlparse

import time

from urllib.request import urlopen

import re

import lxml.html

from scrapy.exceptions import CloseSpider

from scrapy_redis.spiders import RedisSpider 

# 1.获取spider的url列表
# 2.由url初始化的request经过middleware的处理,产生reponse,则到步骤4
# 3.request经过下载器返回reponse
# 4.reponse传递给spider的parse函数，产生item则步骤5，产生resquest则步骤3
# 5.item传递给pipeline与扩展方法进行处理

# 开启爬虫会调用Spider的spider_opened方法
class DmozSpider(scrapy.spiders.Spider):
    name = 'csdnarticle'
    file_name = 'csdn'
    state = {"item_cnt":0}
    allowed_domains = ["csdn.net"]
    # 每个url绑定一个scrapy的request对象，request对象将返回结果
    # 作为参数调用parse函数
    start_urls = ['https://www.csdn.net']

    # 某些网站可能需要http认证
    # http_user = 'user'
    # http_pass = 'pass'

    def __init__(self):
        super().__init__(self)
        # 获取网站中指定数量的链接
        self.get_links(url='https://www.csdn.net', reg_link=re.compile(r'<a[\s]+href="(.*?)".*?</a>'), max_link=20)
        self.start_urls = list(set(self.start_urls))

    # parse方法中如果返回request，则会继续调用downloader handler处理该request
    # response被传递给其他parse处理时，应该能被序列化，在lambda函数中就不能被序列化
    # 所以Request的的callback参数应该直接指向回调函数，而不是lambda
    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open('myfile/'+filename, 'wb') as f:
        #     f.write(response.body)

        # 自定义属性，如果指定了JOBDIR，则保存spider状态的时候
        # spider的自定义属性也会保存进去
        self.state['item_cnt'] = self.state.get('item_cnt', 0) + 1

        xpath_div = '//div[@class="nav_com"]/ul/li'
        xpath_main = '//main/ul/li/*/*/*/a'
        # 返回xpath selector列表，response.css：选择css选择器，response.selector.xpath：选择xpath选择器
        # selector其实是一个根据xml节点生成的生成器( scrapy.utils.iterators.xmliter)，
        # 而普通的xpath会建立整个dom文档树，对于大数据量的html来说，由于是一级一级往下找，速度慢且消耗很大的内存
        # 类似的大数据量文件如csv，也可以以行为单位存进生成器中，遍历时可以优化内存
        for sel in response.xpath(xpath_main):
            # 基于上层xpath使用绝对路径,也可以使用sel.xpath(.//div)指定
            # title = sel.xpath('/div/div/h2/a/text()').extract()
            # descendant指示子孙标签，根据子孙标签查找父标签
            # title = sel.xpath('/div[descendant::div[contains(@class, 'title')]]/div/h2/a/text()').extract()
            # 选择h2下第一个a标签
            # title = sel.xpath('/div/div/h2/a[1]/text()').extract()
            # 选择/div/div/h2/a下第一个a标签
            # title = sel.xpath('(/div/div/h2/a)[1]/text()').extract()
            # 此方式也可以选择出text的内容
            # title = sel.xpath('string(/div/div/h2/a)').extract()
            # title = sel.xpath('/div/div/h2/a/text()').re('[a-zA-Z0-9]')
            # 结合css选择器使用
            # title = sel.css('div.feedlist_mod').xpath('./div/h2/a/text()').re('[a-zA-Z0-9]')
            # link = sel.xpath('/div/div/h2/a/@href').extract()
            # 在选择器上使用re命名空间里的正则表达式
            # link = sel.xpath('/div/div/h2/a[re:test(@href, "[\d]+$")]/@href').extract()
            # 自定义命名空间
            #sel.register_namespace('c':'https://www.csdn.net/nav/db')
            # link = sel.xpath('//c:link').extract()
            # 当选择如//link节点时，可能没有数据，因为命名空间被覆盖,//link其实是在命名控制中查找，需要去除
            # 但这样会消耗性能，这是因为要修改文件的所有节点
            #sel.remove_namespaces()
            # link = sel.xpath('/div[contains(@class,'list_con')]/div/h2/a/@href').extract()
            #print('mylog---:',title, link)

            # 返回类字典对象，可以使用常用的dict API方法
            item = DmozItem()
            # 赋初始值
            #item = DmozItem(title="", link="")

            # unicode编码为utf-8
            item['title'] = sel.xpath('text()')[0].extract().replace('\n','').strip()
            item['link'] = urljoin(response.url, sel.xpath('@href')[0].extract())

            # 保存后的item可以用于存储，1:在scrapy 命令指定-o选项，2:在pippeline中自定义处理
            yield item

        # 使用ItemLoader提取数据到item中，解析得到多个结果时，后面的结果会append到之前的数据中
        # 处理的过程中使用输入器与输出器,可以自定义输入输出器
        # l = ItemLoader(item=DmozItem(), response=response)
        # l.add_xpath('title', '//main/ul/li/div/div/h2/a/text()')
        # l.add_xpath('link', '//main/ul/li/div/div/h2/a/@href')
        # l.add_css('desc', 'title')
        # # 添加固定值
        # l.add_value('date', 'today')

        # return l.load_item()

    def get_links(self, url=None, reg_link=None, max_link=10):
        html = urlopen(url).read().decode()
        links = reg_link.findall(html)
        links = [urljoin(url, link) for link in links]
        links = [link for link in links if urlparse(link).netloc.find('csdn') != 0]
        self.start_urls.extend(links)

        if max_link <= len(self.start_urls): return
        for link in links:
            self.get_links(link, max_link)

class CSDNImageSpider(scrapy.spiders.Spider):
    name = 'csimage'
    allowed_domains = ['www.douban.com']
    start_urls = ["https://www.douban.com/"]

    def parse(self, response):
        item = CSDNItemImg()
        # 根据response在浏览器中打开url
        # from scrapy.utils.response import open_in_browser
        # open_in_browser(response)
        # 在shell终端调试，会屏蔽scrapy引擎，所以不能使用fetch命令
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        for sel in response.xpath('//img'):
            item['image_urls'] = sel.xpath('@src').extract()
            yield item

# 实现表单的登录，如果表单需要与cookie数据对比，则在setting中开启cookie
class LoginSpider(scrapy.spiders.Spider):
    name = 'example.com'
    allowed_domains = ['example.webscraping.com']
    start_urls = ["http://example.webscraping.com/places/default/user/login"]

    def parse(self, response):
        formdata = self.getFormData(response.body)
        formdata['email'] = 'test123@test.com'
        formdata['password'] = 'test'
        return scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.afterlogin
        )

    def getFormData(self, html):
        tree = lxml.html.fromstring(html.decode())
        data = {}
        for e in tree.cssselect('form input'):
            if e.get('name'):
                data[e.get('name')] = e.get('value')
        return data

    def afterlogin(self, response):
        if "user/login" in response.url:
            self.logger.info('Login failed')
            # 此异常抛出后，spider会close掉
            raise CloseSpider('Login failed')
            #return
        
# 基于redis的的分布式爬虫
class CDSNRedisSpider(RedisSpider):
    name = 'csdnredis'
    allowed_domains = ['www.douban.com']

    # 对应redis数据库的key,指定从redis数据库哪个keys中获取
    # url,如果redis_key队列为空，爬虫会一直处于空跑状态
    # 可在自定义扩展方法中判断是否退出爬虫
    redis_key = 'csdnredis:start_urls'

    def parse(self, response):
        item = CSDNItemImg()
        for sel in response.xpath('//img'):
            item['image_urls'] = sel.xpath('@src').extract()
            yield item

class Proxy_Youdaili_Spider(scrapy.spiders.Spider):
    name = 'proxy_youdaili'
    allowed_domains = ['www.youdaili.net']
    
    start_urls = ['https://www.youdaili.net/Daili/http/36803.html']
    
    def parse(self, response):
        item = ProxyItem()

        xpath = '//div[@class="content"]/p'
        for sel in response.xpath(xpath):
            item['ipport'] = sel.xpath('text()').extract()
            yield item

class TaobaoSpider(scrapy.spiders.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['https://www.taobao.com/']

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse, dont_filter=True)

    def parse(self, reponse):
        pass