# -*- coding: utf-8 -*-

# Scrapy settings for srppro project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'srppro'

SPIDER_MODULES = ['srppro.spiders']
NEWSPIDER_MODULE = 'srppro.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'srppro (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 延时并不是精确的，因为精确的请求同样会被反爬虫检测到，
# 所以在每个延时中间添加随机的偏移量
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

# telnet配置
TELNETCONSOLE_PORT = [6023, 6073]
TELNETCONSOLE_HOST = '127.0.0.1'

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'srppro.middlewares.SrpproSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'srppro.middlewares.SrpproDownloaderMiddleware': 543,
#}

DOWNLOADER_MIDDLEWARES = {
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 127,
    'srppro.middlewares.UAPOOLS': 126,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# 通用扩展，其他通用扩展还有logstats基本统计信息扩展，发送邮件，内存调试扩展等，
# None不启用，但扩展可能也会受到其他设置的影响，导致扩展不生效
# 如以下TelnetConsole扩展依赖TELNETCONSOLE_ENABLED
# 有些扩展如果依赖项设置了，则会默认开启
EXTENSIONS = {
    #'scrapy.extensions.telnet.TelnetConsole': 1,
    #'scrapy.extensions.closespider.CloseSpider': 1,
    #'scrapy.extensions.statsmailer.StatsMailer': 1,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'srppro.pipelines.SrpproPipeline': 300,
#}

ITEM_PIPELINES = {
   #'srppro.pipelines.SrpproPipeline': 300,
   #'srppro.pipelines.MongoPipeline': 301,
   #'srppro.pipelines.CSDNImagesPipeline': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'myfile/httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
# http缓存放入本地文件中
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# 使用Dummy缓存策略，每次都从缓存读取
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.DummyPolicy'
# 使用Dummy缓存策略，根据响应头数据设置缓存
#HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy'

# mongodb数据库
MONGO_URI = 'localhost'
MONGO_DATABASE = 'CSDN'

# 图片参数
IMAGES_STORE = "myfile/image"
IMAGES_EXPIRES = 2
# 缩略尺寸
IMAGES_THUMBS = {
    'small':(50, 50),
    'big':(250, 250),
}
# 根据大小限制图片下载
IMAGES_MIN_HEIGHT = 50
IMAGES_MIN_WIDTH = 50

# closespider扩展配置
#CLOSESPIDER_ITEMCOUNT = 5
# CLOSESPIDER_TIMEOUT = 30
# CLOSESPIDER_PAGECOUNT = 5
# CLOSESPIDER_ERRORCOUNT = 10

# 邮件扩展配置
STATSMAILER_RCPTS = '1764740905@qq.com'

# 发送邮件的服务器
MAIL_HOST = 'smtp.qq.com'
# 邮件发送者
MAIL_FROM = '1764740905@qq.com'
# 发送端口号
MAIL_PORT = 25
# 登录到stmp服务需要的验证信息
MAIL_PASS = ""
MAIL_USER = "1764740905@qq.com"

# 网站连接广度优先爬取设定，默认是深度优先
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'