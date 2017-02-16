import requests
import scrapy
import threading
import redis
import ast
import json
import time
from settings import redis_pool
from models import BtaPrice

# response = requests.get(url)
# html = Selector(text=response.text)
# rating_list = html.xpath('//tr[contains(@id, "ctl00_ContentHolder_rptGradeDoc_ctl")]')
# page_list = html.xpath('//tr[contains(@id, "ctl00_ContentHolder_pgrBoardPager_PagerList_ct")]')
# page_next = html.xpath('//a[@style="font-weight:bold;color:#353959;font-size:12px;border-color:#353959;background:#f8f9fb;"]/following-sibling::a[1]')

class HumbleBundleCrawler(threading.Thread):

    def __init__(self, key):
        self.key = key
        threading.Thread.__init__(self)
        self.init()
        self.urls = []

    def init (self):
        self.redis = redis.Redis(connection_pool=redis_pool)
        self.site = self.redis.hscan('bta_site:{}'.format(self.key))[1]
        self.url = self.site.get(b'url').decode('utf-8')

    def init_parse (self):
        response = requests.get(self.url)
        html = scrapy.Selector(text=response.text)
        categories = html.xpath(self.site.get(b'xpath_category').decode('utf-8')).extract()[0:-2]
        for category in categories:
            try:
                self.parse(self.url+category)
            except Exception as e:
                print (e)

    def parse (self, url):
        if url not in self.urls :
            response = requests.get(url)
            html = scrapy.Selector(text=response.text)
            bta_price = BtaPrice()
            bta_price.url = html.xpath(self.site.get(b'xpath_url').decode('utf-8')).extract().pop()
            bta_price.title = html.xpath(self.site.get(b'xpath_title').decode('utf-8')).extract().pop()
            bta_price.total = html.xpath(self.site.get(b'xpath_total').decode('utf-8')).re('([G0-9.,]+)').pop().replace(',', '')
            bta_price.purchases = html.xpath(self.site.get(b'xpath_purchases').decode('utf-8')).re('([G0-9.,]+)').pop().replace(',', '')
            bta_price.average = html.xpath(self.site.get(b'xpath_average').decode('utf-8')).re('([G0-9.,]+)').pop().replace(',', '')
            html.xpath(self.site.get(b'xpath_start_end').decode('utf-8')).re(self.site.get(b're_start_end').decode('utf-8'))  # 시작 종료 timestamp
            bta_price.time = int(time.time())

            print(bta_price)

            self.urls.append(bta_price.url)
            next_page = html.xpath(self.site.get(b'xpath_next_page').decode('utf-8')).extract_first()
            if (next_page) :
                self.parse(self.url+next_page)

    def save(self):
        pass

    def run(self):
        self.init_parse()

if __name__ == '__main__':
    HumbleBundleCrawler('www.humblebundle.com').start()