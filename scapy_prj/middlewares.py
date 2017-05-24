# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


_IP_INDEX_ = 0
IPS = [
"162.243.128.154:8080",
"200.150.68.126:3128",
"111.23.10.45:80",
"186.95.182.59:8080",
"222.94.146.102:808",
"187.75.231.53:8080",
"212.237.27.50:1189",
"36.249.28.137:808",
"183.88.212.184:8080",
"113.227.183.167:80",
]

class ScapyPrjSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    

class MyCustomDownloaderMiddleware(object):
    def process_request(self, request, spider):

        # Set the location of the proxy
        global _IP_INDEX_

        request.meta['proxy'] = "http://" + IPS[_IP_INDEX_]
        _IP_INDEX_ = (_IP_INDEX_+1) % len(IPS)


