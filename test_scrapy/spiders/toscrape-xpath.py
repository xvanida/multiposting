# -*- coding: utf-8 -*-
import scrapy
from .. import settings

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = ['http://jobs.careerpage.fr/career/multiposting-%s-fr/' % url for url in settings.TYPE_INFO]

    def parse(self, response):
        for link in response.css('td.view a::attr(href)').extract():
            id = link.split('/')[-2] #id of the offer
            request = scrapy.http.Request("http://jobs.careerpage.fr" + link, callback=self.get_infos)
            request.meta['id_offer'] = id
            request.meta['url_name'] = next(url for url in settings.TYPE_INFO if url in response.url)
            yield request

    def get_infos(self, response):
        item = dict()
        item['url_name'] = response.meta['url_name']
        item['title'] = response.xpath('//div[@class="header"]/h2/text()').extract_first()
        item['reference'] = response.meta['id_offer']
        item['publication_date'] = response.xpath('//div[@class="advanced-search"]/li[1]/span[@class="value"]/text()').extract_first()
        item['location_name'] = response.xpath('//div[@class="advanced-search"]/li[1]/span[@class="value"]/text()').extract_first()
        item['country'] = "France"
        item['postal_code'] = response.xpath('//div[@class="advanced-search"]/li[1]/span[@class="value"]/text()').extract_first()
        item['education_level'] = response.xpath('//div[@class="advanced-search"]/li[3]/span[@class="value"]/text()').extract_first()
        item['experience_level'] = response.xpath('//div[@class="advanced-search"]/li[4]/span[@class="value"]/text()').extract_first()
        item['contract_type'] = response.xpath('//div/span[@class="value"]/text()').extract_first()
        item['job_description'] = response.xpath('//ul[@class="content description"]/p/text()').extract()
        yield item
