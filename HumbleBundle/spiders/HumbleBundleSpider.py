import scrapy
import time
from HumbleBundle.items import HumbleBundleItem

class HumbleBundleSpider(scrapy.Spider):
    name = 'humblebundlespider'
    start_urls = [
        'https://www.humblebundle.com',
        'https://www.humblebundle.com/books'
    ]

    def parse(self, response):
        yield HumbleBundleItem(
            url=response.xpath('//meta[@property="og:url"]/@content').extract().pop(),
            title=response.xpath('//meta[@property="og:title"]/@content').extract().pop(),
            total_payments=response.xpath('//td[@class="st-td js-statistics-total-payments"]/text()').re('([G0-9.,]+)').pop().replace(',', ''),
            num_purchases=response.xpath('//td[@class="st-td js-statistics-num-purchases"]/text()').re('([G0-9.,]+)').pop().replace(',', ''),
            average_purchase=response.xpath('//td[@class="st-td js-statistics-average-purchase"]/text()').re('([G0-9.,]+)').pop().replace(',', ''),
            time=int(time.time())
        )
        next_page = response.xpath('//div[@id="subtab-container"]/a[not(contains(@href, "#"))]/@href').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)