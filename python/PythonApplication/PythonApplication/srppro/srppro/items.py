# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

def serialize_population(value):
    return 'num %s' % str(value)

class SrpproItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    # 使用自定义的函数对item进行序列化
    population = scrapy.Field(serializer=serialize_population)

class DmozItem(scrapy.Item):
    title = scrapy.Field(default=None)
    link = scrapy.Field()
    #desc = scrapy.Field()
    #date = scrapy.Field()

# 图片组
class CSDNItemImg(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()