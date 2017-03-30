# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MzitucrawlerPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'mzitu.all':
            return item
        elif spider.name == 'mzitu.zipai':
            return item



class MzituCrawlerImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_urls'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_name = request.url.split('/')[-1]
        image_dir = item['image_title']
        image_no = item['image_no']
        dir = str(image_dir) + "_" + str(image_no)
        #image_name = str(image_guid).split('.')[0]
        #image_name = image_name + '.jpg'
        #filename = u'full/{0}/{1}'.format(item['title'], image_guid)  # title为二级目录
        #filename = u'{}/{}'.format(FolderName, image_guid)
        filename = u'{}/{}/{}/{}'.format('Mzitu',u'每日更新',dir,image_name)
        return filename

class MzituCrawlerZiPaiImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_urls'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_name = request.url.split('/')[-1]
        image_dir = item['image_title']
        dir = str(image_dir)
        filename = u'{}/{}/{}'.format('Mzitu',u'自拍',image_name)
        return filename


class GankIoImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_urls'] = image_paths
        return item


    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = request.url.split('/')[-1]
        image_name = str(image_guid).split('.')[0]
        filename = u'{}/{}/{}'.format('Gank.io',u'福利',image_guid)
        return filename
