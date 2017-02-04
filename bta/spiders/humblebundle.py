# -*- coding: utf-8 -*-
import scrapy
import time
from bta.items import BtaItem

class HumbleBundleSpider(scrapy.Spider):
    name = 'humblebundle'
    allowed_domains = ["https://www.humblebundle.com"]
    start_urls = [
        'https://www.humblebundle.com',
        'https://www.humblebundle.com/books'
    ]

    def parse(self, response):
        yield BtaItem(
            url=response.xpath('//meta[@property="og:url"]/@content').extract().pop(),
            title=response.xpath('//meta[@property="og:title"]/@content').extract().pop(),
            total=response.xpath('//td[@class="st-td js-statistics-total-payments"]/text()').re('([G0-9.,]+)').pop().replace(',', ''),
            purchases=response.xpath('//td[@class="st-td js-statistics-num-purchases"]/text()').re('([G0-9.,]+)').pop().replace(',', ''),
            average=response.xpath('//td[@class="st-td js-statistics-average-purchase"]/text()').re('([G0-9.,]+)').pop().replace(',', ''),
            time=int(time.time())
        )
        next_page = response.xpath('//div[@id="subtab-container"]/a[not(contains(@href, "#"))]/@href').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)