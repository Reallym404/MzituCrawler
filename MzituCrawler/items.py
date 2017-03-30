# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MzitucrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field()
    image_title = scrapy.Field()
    image_years = scrapy.Field()
    image_no = scrapy.Field()


class MzituZiPaicrawlerItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_title = scrapy.Field()


class GankiomeizhiItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field()
    pass
