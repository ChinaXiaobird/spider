# -*- coding: utf-8 -*-
import scrapy


class TaocheSpider(scrapy.Spider):
    name = 'taoche'
    allowed_domains = ['taoche.com']
    start_urls = ['http://taoche.com/']

    def parse(self, response):
        pass
