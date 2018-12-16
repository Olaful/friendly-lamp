# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SrpproItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    population = scrapy.Field()

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    date = scrapy.Field()