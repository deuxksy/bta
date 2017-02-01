# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BtaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    total_payments = scrapy.Field()
    num_purchases = scrapy.Field()
    average_purchase = scrapy.Field()
    time = scrapy.Field()
