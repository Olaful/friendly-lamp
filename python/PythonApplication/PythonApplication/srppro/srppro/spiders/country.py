# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from srppro.items import SrpproItem

class CountrySpider(CrawlSpider):
    # 爬虫名称
    name = 'country'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/view/Australia-14',
                  'http://example.webscraping.com/places/default/view/American-Samoa-5']

    rules = (
        # 正则匹配网站下的网址，只向特定的网址发送请求
        Rule(LinkExtractor(allow=r'/index/', deny=r'/user/', ), follow=True),
        # 将响应发给callback函数处理
        Rule(LinkExtractor(allow=r'/view/', deny=r'/user/', ), callback='parse_item', follow=True),
    )

    # 自定义解析结果
    def parse_item(self, response):
        item = SrpproItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()

        name_css = 'tr#places_country__row td.w2p_fw::text'
        # 也支持xpath解析
        item['name'] = response.css(name_css).extract()
        population_css = 'tr#places_population__row td.w2p_fw::text'
        item['population'] = response.css(population_css).extract()

        return item
