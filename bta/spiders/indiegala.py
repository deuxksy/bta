# -*- coding: utf-8 -*-
import scrapy


class IndiegalaSpider(scrapy.Spider):
    name = "indiegala"
    allowed_domains = ["https://www.indiegala.com/"]
    start_urls = ['http://https://www.indiegala.com//']

    def parse(self, response):
        pass
