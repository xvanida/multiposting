# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import CsvItemExporter
from . import settings

class TestScrapyPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.exporters = {}
        for url in settings.TYPE_INFO:
            my_file = open('multiposting-%s-fr.csv' % url, 'w+b')
            exporter = CsvItemExporter(my_file)
            exporter.start_exporting()
            self.exporters[url] = exporter

    def spider_closed(self, spider):
        for _, exporter in self.exporters.items():
            exporter.finish_exporting()
#        self.file.close()

    def process_item(self, item, spider):
        print("DEBUG")
        print(item)
        print("_______________")
        self.exporters[item['url_name']].export_item(item)
        return item
