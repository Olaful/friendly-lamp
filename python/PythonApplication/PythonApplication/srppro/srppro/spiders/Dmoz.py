import scrapy

from srppro.items import DmozItem, CSDNItemImg

from scrapy.loader import ItemLoader

from urllib.parse import urljoin

# 处理过程：1.spider的parse函数产生item; 2.到setting文件中查找ITEM_PIPELINES
# 3.从 ITEM_PIPELINES中找出pipeline来处理
class DmozSpider(scrapy.spiders.Spider):
    name = 'dmoz'
    file_name = 'csdn'
    allowed_domains = ["csdn.net"]
    # 每个url绑定一个scrapy的request对象，request对象将返回结果
    # 作为参数调用parse函数
    start_urls = ["https://www.csdn.net"]

    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open('myfile/'+filename, 'wb') as f:
        #     f.write(response.body)

        # 返回xpath selector列表，response.css：选择css选择器，response.selector.xpath：选择xpath选择器
        for sel in response.xpath('//div[@class="nav_com"]/ul/li'):
            # 基于上层xpath使用绝对路径,也可以使用sel.xpath(.//div)指定
            # title = sel.xpath('/div/div/h2/a/text()').extract()
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

            item = DmozItem()
            # unicode编码为utf-8
            item['title'] = sel.xpath('a/text()')[0].extract()
            item['link'] = urljoin(response.url, sel.xpath('a/@href')[0].extract())

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

class CSDNImageSpider(scrapy.spiders.Spider):
    name = 'csimage'
    allowed_domains = ['csdn.net']
    start_urls = ["https://www.csdn.net"]

    def parse(self, response):
        item = CSDNItemImg()
        for sel in response.xpath('//img'):
            item['image_urls'] = sel.xpath('@src').extract()
            yield item
        