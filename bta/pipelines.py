# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from bta.settings import pool
import redis
import json


class BtaPipeline(object):
    def process_item(self, item, spider):
        r = redis.Redis(connection_pool=pool)
        url = item['url']
        if url and url.split('//'):
            if 2 == len(url.split('//')[-1].split('/')):
                key = ':top:'.join(url.split('//')[-1].split('/'))
            else:
                key = ':'.join(url.split('//')[-1].split('/'))
        else:
            key = url
        r.lpush('bta_price:{}'.format(key), item.toJSON())
        return item
