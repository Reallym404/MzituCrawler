import scrapy
import json
from MzituCrawler.items import GankiomeizhiItem

# Gank.Io 爬虫. 自动终止有点问题 需改进
class GankIoSpider(scrapy.Spider):
    name = 'Gank.Io'
    allowed_domains = ["gank.io"]
    index = 1
    baseUrl = 'http://gank.io/api/data/福利/50/'
    start_urls = [baseUrl + str(index)]

    custom_settings = {
        'ITEM_PIPELINES': {'MzituCrawler.pipelines.GankIoImagePipeline': 200, }
    }

    def parse(self, response):

        item = GankiomeizhiItem()

        jsonData = json.loads(response.body_as_unicode())
        results = jsonData.get('results')
        if len(results) == 0:
            self.log(u'数据已全部加载完毕,共%s页....'%str(self.index))
            exit()
        self.log(u'正在解析第%s页数据' % str(self.index))
        for o in results:
            item['image_urls'] = [o.get('url')]
            item['image_name'] = o.get('_id')

            yield item

        self.index +=1
        url_next = self.baseUrl + str(self.index)
        yield scrapy.Request(url=url_next)