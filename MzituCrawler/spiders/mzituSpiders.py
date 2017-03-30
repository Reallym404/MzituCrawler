import scrapy
#from scrapy.contrib.spiders import CrawlSpider,Rule
#from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from MzituCrawler.items import MzitucrawlerItem
import re

# 妹子图每日更新
class MzituSpider(scrapy.Spider):

    name = 'mzitu.all'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/all']
    """
    rules = (
        #http://www.mzitu.com/34510
        Rule(LinkExtractor(allow=r"www.mzitu.com/\d*$"), callback="parse_every_day", follow=True),
    )
    """

    url_list = []

    def parse(self, response):
        selector = Selector(response=response)
        urls_list = []
        ul_list = selector.xpath('//ul[@class="archives"]')
        for ul in ul_list:
            a_list = ul.xpath('./li/p/a/@href').extract()
            for a in a_list:
                urls_list.append(str(a))
        for day_url in urls_list:
            yield scrapy.Request(url=day_url, callback=self.parse_every_day)



    def parse_every_day(self,response):
        self.log('every day page url:%s'% response.url)
        url = response.url
        selector = Selector(response=response)
        page = selector.xpath('//div[@class="pagenavi"]/a/span/text()').extract()[-2:-1]
        page_count = page[0]
        for i in range(1,int(page_count) + 1):
            yield scrapy.Request(url=url+'/'+str(i), callback=self.parse_every_page)


    def parse_every_page(self,response):
        self.log('every page url:%s' % response.url)
        url = response.url
        regex = ".com/\d*/"
        regexobject = re.compile(regex)
        no = regexobject.search(url).group().split('/')[1]
        item = MzitucrawlerItem()
        selector = Selector(response=response)
        title = selector.xpath('//div[@class="content"]/div[@class="main-image"]/p/a/img/@alt').extract()[0]
        url = selector.xpath('//div[@class="main"]/div[@class="content"]/div[@class="main-image"]/p/a/img/@src').extract_first()
        name = url.split('/')[-1]

        item['image_urls'] = [url]
        item['image_name'] = name
        item['image_title'] = title
        item['image_no'] = no

        yield item

