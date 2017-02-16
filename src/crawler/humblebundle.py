from settings import redis_pool
from settings import config
from models import BtaPrice
from commons import log
import requests
import scrapy
import threading
import redis
import time
import traceback
import logging
import os

logger = log.get_logger(logger=logging.getLogger(os.path.basename(__file__).split('.')[0]), config=config)

class HumbleBundleCrawler(object):

    def __init__(self, key):
        self.key = key
        self.urls = []
        self.encoding = 'utf-8'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        # threading.Thread.__init__(self)
        self.init()

    def init (self):
        self.redis = redis.Redis(connection_pool=redis_pool)
        self.site = self.redis.hscan('bta_site:{}'.format(self.key))[1]
        self.url = self.site.get(b'url').decode(self.encoding)

    def init_parse (self):
        response = requests.get(self.url, headers=self.headers)
        html = scrapy.Selector(text=response.text)
        categories = html.xpath(self.site.get(b'xpath_category').decode(self.encoding)).extract()[0:-2]
        for category in categories:
            try:
                self.parse(self.url+category)
            except Exception:
                logger.error(traceback.format_exc())

    def parse (self, url):
        if url not in self.urls :
            response = requests.get(url)
            html = scrapy.Selector(text=response.text)

            bta_price = BtaPrice()
            bta_price.url = html.xpath(self.site.get(b'xpath_url').decode(self.encoding)).extract().pop()
            bta_price.title = html.xpath(self.site.get(b'xpath_title').decode(self.encoding)).extract().pop()
            bta_price.total = html.xpath(self.site.get(b'xpath_total').decode(self.encoding)).re(self.site.get(b're_number').decode(self.encoding)).pop().replace(',', '')
            bta_price.purchases = html.xpath(self.site.get(b'xpath_purchases').decode(self.encoding)).re(self.site.get(b're_number').decode(self.encoding)).pop().replace(',', '')
            bta_price.average = html.xpath(self.site.get(b'xpath_average').decode(self.encoding)).re(self.site.get(b're_number').decode(self.encoding)).pop().replace(',', '')
            bta_price.time = int(time.time())

            html.xpath(self.site.get(b'xpath_start_end').decode(self.encoding)).re(self.site.get(b're_start_end').decode(self.encoding))  # 시작 종료 timestamp
            logger.debug(bta_price.url)
            self.urls.append(bta_price.url)
            self.save(bta_price)
            next_page = html.xpath(self.site.get(b'xpath_next_page').decode(self.encoding)).extract_first()
            if (next_page) :
                self.parse(self.url+next_page)

    def save(self, bta_price):
        url = bta_price.url
        if url and url.split('//'):
            key_split = url.split('//')[-1].split('/')
            if 2 == len(key_split):
                key = ':top:'.join(key_split)
            else:
                key = ':'.join(key_split)
        else:
            key = url
        self.redis.lpush('bta_price:{}'.format(key), bta_price.toJSON())

    def run(self):
        self.init_parse()