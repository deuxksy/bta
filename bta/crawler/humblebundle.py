import logging
import os
import time
import traceback

import redis
import requests
import scrapy
from kiki.commons import log
from kiki.commons import proxy
from kiki.commons.util import web
from requests.exceptions import ProxyError

from bta.config import config
from bta.models import BtaPrice
from bta.settings import redis_pool_bta

logger = log.get_logger(logger=logging.getLogger(os.path.basename(__file__).split('.')[0]), config=config)


class HumbleBundleCrawler(object):
    def __init__(self, key):
        self.key = key
        self.encoding = 'utf-8'
        self.urls = []
        # threading.Thread.__init__(self)
        self.init()

    def init(self):
        self.headers = {'User-Agent': web.get_user_agent()}
        self.redis = redis.Redis(connection_pool=redis_pool_bta)
        self.site = self.redis.hscan('bta_site:{}'.format(self.key))[1]
        self.url = self.site.get(b'url').decode(self.encoding)
        self.proxies = proxy.get_proxies()
        self.count = {}

    def get_response(self, url, max=2):
        """Sends a GET request.

        :param url:
        :param max: (optional)
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        response = None

        # url 별 재시도 회수를 저장 하지 위한 count 값
        if url not in self.count:
            self.count[url] = 0

        # max(2) 보다 크면 proxy 를 사용하지 않고 그냥 가지고 오기
        if max < self.count[url]:
            # url count 삭제
            self.count.pop(url)
            return requests.get(url=url, headers=self.headers)

        try:
            response = requests.get(url=url, headers=self.headers, proxies=self.proxies)
        except ProxyError:
            response = requests.get(url=url, headers=self.headers, proxies=self.proxies)
        finally:
            if response is None:
                self.count[url] += 1
                self.proxies = proxy.get_proxies()
                return self.get_response(url)
            else:
                return response

    def init_parse(self):
        response = self.get_response(url=self.url)
        if response is not None:
            html = scrapy.Selector(text=response.text)
            categories = html.xpath(self.site.get(b'xpath_category').decode(self.encoding)).extract()[0:-2]
            for category in categories:
                try:
                    self.parse(self.url + category)
                except Exception:
                    logger.error(traceback.format_exc())

    def parse(self, url):
        if url not in self.urls:
            response = self.get_response(url=url)
            if response is None:
                return -1

            html = scrapy.Selector(text=response.text)

            bta_price = BtaPrice()
            bta_price.url = html.xpath(self.site.get(b'xpath_url').decode(self.encoding)).extract().pop()
            logger.debug(bta_price.url)
            bta_price.title = html.xpath(self.site.get(b'xpath_title').decode(self.encoding)).extract().pop()
            bta_price.total = html.xpath(self.site.get(b'xpath_total').decode(self.encoding)).re(
                self.site.get(b're_number').decode(self.encoding)).pop().replace(',', '')
            bta_price.purchases = html.xpath(self.site.get(b'xpath_purchases').decode(self.encoding)).re(
                self.site.get(b're_number').decode(self.encoding)).pop().replace(',', '')
            bta_price.average = html.xpath(self.site.get(b'xpath_average').decode(self.encoding)).re(
                self.site.get(b're_number').decode(self.encoding)).pop().replace(',', '')
            bta_price.time = int(time.time())

            html.xpath(self.site.get(b'xpath_start_end').decode(self.encoding)).re(
                self.site.get(b're_start_end').decode(self.encoding))  # 시작 종료 timestamp
            self.urls.append(bta_price.url)
            self.save(bta_price)
            next_page = html.xpath(self.site.get(b'xpath_next_page').decode(self.encoding)).extract_first()
            if (next_page):
                self.parse(self.url + next_page)

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
        logger.debug(bta_price.toJSON())
        self.redis.lpush('bta_price:{}'.format(key), bta_price.toJSON())

    def run(self):
        self.init_parse()
