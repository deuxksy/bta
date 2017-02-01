# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from bta.settings import pool
import redis

class BtaPipeline(object):
    def process_item(self, item, spider):
        r = redis.Redis(connection_pool=pool)
        url = item['url']
        if url and url.split('//'):
            key = ':'.join(url.split('//')[-1].split('/'))
        else:
            key = url
        r.lpush(key, item)
        return item