# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

import random
import base64

# 中间件负责处理request与response,如果不启用，requesr将不会经过中间件的处理

class SrpproSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SrpproDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # crawler可以访问scrapy的核心组件，其要使用spider与spider的settings进行实例化
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        # 解除信号与函数的关联
        #crawler.signals.disconnect(s.spider_opened, signal=signals.spider_opened)
        # 取消该信号的所有关联
        #crawler.signals.disconnect_all(s.spider_opened)
        # 发送一个信号，kwargs参数会传递给connect中的处理函数
        #crawler.signals.send_catch_log(signals.spider_opened, *kwargs)
        return s

    # 如果返回response，则scrapy引擎不会调用其他process_request方法，执行process_response方法
    # 所以可在此返回自己本地的response，这样就不用再请求网络了
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # 重定向
        request.meta['dont_redirect'] = True
        # 重试
        request.meta['dont_retry'] = True
        # 过滤出不在spider的allowed_domains的url
        request.meta['dont_filter'] = True
        # 重定向的url
        request.meta['redirect_urls'] = ['https://www.baidu.com', 'https://www.douban.com/']
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# UserAgent设置中间件
class UAPOOLS(UserAgentMiddleware):
        def __init__(self, user_agent=''):
            self.user_agent = random.choice([
                            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'])
                            # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                            # 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
                            # 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
                            # 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
                            # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                            # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                            # 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                            # 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
                            # 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'])

# 用户代理设置中间件
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://119.254.88.53:8080"
        proxy_user_pass = "USERNAME:PASSWORD"
        #encoded_user_pass = base64.encodestring(proxy_user_pass)
        encoded_user_pass = base64.b64encode(proxy_user_pass.encode()).decode("ascii")
        #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
