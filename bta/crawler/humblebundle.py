#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import time
import traceback

import redis
import scrapy
from kiki.commons import log

from bta.config import config
from bta.crawler import BaseCrawler
from bta.models import BtaDeal
from bta.models import BtaPrice
from bta.settings import redis_pool_bta

logger = log.get_logger(logger=logging.getLogger(os.path.basename(__file__).split('.')[0]), config=config)


class HumbleBundle(BaseCrawler):
    # redis bta db1 접속
    r = redis.Redis(connection_pool=redis_pool_bta)

    def __init__(self, *args, **kwargs):
        super(HumbleBundle, self).__init__(*args, **kwargs)
        self.init()

    def init(self):
        logger.debug('bta_site:{site}'.format(site=self.site))
        self.site = self.r.hscan('bta_site:{site}'.format(site=self.site))[1]
        self.url = self.site.get(b'url').decode(self.encoding)

    def check_price(self):
        response = self.get_response(url=self.url)
        if response is not None:
            html = scrapy.Selector(text=response.text)
            categories = html.xpath(self.site.get(b'xpath_category').decode(self.encoding)).extract()[0:-2]
            for category in categories:
                try:
                    self.parse_price(self.url + category)
                except Exception:
                    logger.error(traceback.format_exc())

    def parse_price(self, url):
        logger.debug(url)
        if url not in self.urls:
            response = self.get_response(url=url)
            if response is None:
                return -1

            html = scrapy.Selector(text=response.text)

            bta_price = BtaPrice()
            bta_price.url = html.xpath(self.site.get(b'xpath_url').decode(self.encoding)).extract().pop()
            bta_price.title = html.xpath(self.site.get(b'xpath_title').decode(self.encoding)).extract().pop()
            bta_price.total = html.xpath(self.site.get(b'xpath_total').decode(self.encoding)).re(
                self.site.get(b're_number').decode(self.encoding)).pop().replace(',', '')
            bta_price.purchases = html.xpath(self.site.get(b'xpath_purchases').decode(self.encoding)).re(
                self.site.get(b're_number').decode(self.encoding)).pop().replace(',', '')
            bta_price.average = html.xpath(self.site.get(b'xpath_average').decode(self.encoding)).re(
                self.site.get(b're_number').decode(self.encoding)).pop().replace(',', '')
            bta_price.time_new = int(time.time())
            bta_price.time_update = int(bta_price.time_new)

            start_end = html.xpath(self.site.get(b'xpath_start_end').decode(self.encoding)).re(
                self.site.get(b're_start_end').decode(self.encoding))  # 시작 종료 timestamp
            self.urls.append(bta_price.url)

            bta_deal = BtaDeal()
            bta_deal.bta_site = self.site
            bta_deal.url = bta_price.url
            bta_deal.title = bta_price.title
            bta_deal.start = int(start_end[0])
            bta_deal.end = int(start_end[1])

            self.save_price(bta_price)
            self.merge_deal(bta_deal)

            next_page = html.xpath(self.site.get(b'xpath_next_page').decode(self.encoding)).extract_first()
            if (next_page):
                self.parse_price(self.url + next_page)

    def save_price(self, bta_price):
        url = bta_price.url
        if url and url.split('//'):
            key_split = url.split('//')[-1].split('/')
            if 2 == len(key_split):
                price_key = ':top:'.join(key_split)
            else:
                price_key = ':'.join(key_split)
        else:
            price_key = url
        # logger.debug(bta_price.to_json())
        self.r.lpush('bta_price:{price_key}'.format(price_key=price_key), bta_price.to_json())

    def merge_deal(self, bta_deal):
        bta_deal_key = 'bta_deal:{site}:{deal}'.format(site=self.site, deal=bta_deal.url.split('/')[-1])
        checkpoint = self.r.hlen(name=bta_deal_key)
        # logger.debug('{bta_deal_key}-{checkpoint}'.format(bta_deal_key, checkpoint))
        if checkpoint:
            bta_deal_dict = self.r.hscan(name=bta_deal_key)[1]
            for property in bta_deal_dict:
                key = property.decode()
                if 'time_' not in key:
                    if bta_deal.__dict__.get(key) != bta_deal_dict.get(property):
                        self.r.hset(name=bta_deal_key, key=key, value=bta_deal.__dict__.get(key))
                        self.r.hset(name=bta_deal_key, key='time_update', value=time.time())
        else:
            bta_deal_dict = bta_deal.__dict__
            self.r.hset(name=bta_deal_key, key='time_new', value=time.time())
            for property in bta_deal_dict:
                self.r.hset(name=bta_deal_key, key=property, value=bta_deal_dict.get(property))
            self.r.hset(name=bta_deal_key, key='time_update', value=time.time())

    def run(self):
        self.check_price()