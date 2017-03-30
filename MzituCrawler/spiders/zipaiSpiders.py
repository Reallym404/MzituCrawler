from scrapy.selector import Selector
import scrapy
from MzituCrawler.items import MzituZiPaicrawlerItem


# 妹子图自拍爬虫
class ZipaiSiders(scrapy.Spider):

    name = 'mzitu.zipai'
    allowed_domains = ['www.mzitu.com']
    base_url = 'http://www.mzitu.com/zipai/comment-page-{}#comments'
    start_urls = ['http://www.mzitu.com/zipai']

    custom_settings = {
        'ITEM_PIPELINES': {'MzituCrawler.pipelines.MzituCrawlerZiPaiImagePipeline': 300,}
    }

    def parse(self, response):
        selector = Selector(response=response)
        page_count = selector.xpath(
        '//div[@class="main"]/div[@class="main-content"]/div[@class="postlist"]/div[@id="comments"]/div[@class="pagenavi-cm"]/span[@class="page-numbers current"]/text()').extract_first()
        self.log(u'自拍总共%s页'%page_count)
        for i in range(1,int(page_count)+1):
            self.log(u'当前解析第%d页'%i)
            url = self.base_url.format(str(i))
            yield scrapy.Request(url=url,callback=self.parse_every_page)


    def parse_every_page(self, response):

        selector = Selector(response=response)
        comments = selector.xpath('//div[@class="main"]/div[@class="main-content"]/div[@class="postlist"]/div[@id="comments"]/ul')

        item = MzituZiPaicrawlerItem()
        li_list = comments.xpath('./li')
        for li in li_list:
            url = li.xpath('./div[@class="comment-body"]/p/img/@src').extract_first()
            title = li.xpath('./div[@class="comment-body"]/p/img/@alt').extract_first()
            self.log(u'alt:%s' % title)
            self.log(u'url:%s' % url)
            item['image_urls'] = [url]
            item['image_title'] = title

            yield item



