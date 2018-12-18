# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem, NotConfigured

import scrapy

from scrapy.pipelines.images import ImagesPipeline

import json

import pymongo

from scrapy import signals

# item在spider中被收集后会传到pipeline组件，再此可以对item进行自定义处理
# 需要在setting文件中配置ITEM_PIPELINES使其生效
class SrpproPipeline(object):
    def __init__(self):
        self.file = open('myfile/item.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if item['title']:
            # json序列化
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(line)
            # process_item方法要返回item，否则item无法传递给其他方法处理
            return item
        else:
            raise DropItem('item is None')

# 使用mongodb存储
class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'))

    def open_spider(self, spider):
        'spider 开启后调用'
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        collection_name = spider.__class__.__name__
        self.db[collection_name].drop()

    def close_spider(self, spider):
        'spider 关闭后调用'
        self.client.close()

    def process_item(self, item, spider):
        collection_name = spider.__class__.__name__
        data_insert = {'_id':item["link"], 'title':item['title']}
        try:
            self.db[collection_name].insert(dict(data_insert))
        except pymongo.errors.DuplicateKeyError:
            pass

# 简单去重
class DuplicatesPipeline(object):
    def __init__(self):
        self.link_seen = set()

    def process_item(self, item, spider):
        if item['link'] in self.link_seen:
            raise DropItem('Duplicate item found:{}'.format(item))
        else: 
            return item

# 在from_crawler方法中结合signal事件实现扩展
class MyExtentPipeline(object):
    def __init__(self, item_count):
        self.item_count = item_count
        self.items_scraped = 0

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 100)

        ext = cls(item_count)

        # 添加信号，当spider中某些事件发生时调用相应的处理
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        # item_scraped事件发生时，会把item, spider入参传入item_scraped函数进行调用
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        return ext

    def spider_opened(self, spider):
        spider.log('opened spider {}'.format(spider.name))

    def spider_closed(self, spider):
        spider.log('closed spider {}'.format(spider.name))

    def item_scraped(self, item, spider):
        self.items_scraped += 1

        if self.items_scraped % self.item_count == 0:
            spider.log('scraped {} item'.format(self.items_scraped))

# 图片下载管道，ImagesPipeline->FilesPipeline->MediaPipeline
# 也可以定义其他类型的文件下载管道
class CSDNImagesPipeline(ImagesPipeline):
    # image_urls组中的图片将会被下载，获取所有图片的url,完成后把结果将会以元组的形式传给item_completed方法
    # 元组形式:[(True, {'checksum':'md5 hash', 'path':‘full/sha1 hash', 'url':'image url'}), (XX),..]
    # 保存的图片文件名是经过hash处理过的，也可以重写file_path方法自定义文件名，True下载成功，否则失败
    # 文件没有过期的话不会被重新下载
    # item处理的过程中会被锁定
    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:
            yield scrapy.Request(image_url)
    
    # 获取成功的image路径信息
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')
        item['images'] = image_paths
        return item