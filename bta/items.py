# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import json
import scrapy


class BtaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    total = scrapy.Field()
    purchases = scrapy.Field()
    average = scrapy.Field()
    time = scrapy.Field()

    def toJSON(self, sort_keys=True, indent=4, separators=(',', ':')):
        return json.dumps(dict(self), sort_keys=sort_keys, separators=separators)