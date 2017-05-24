# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


_IP_INDEX_ = 0
IPS = [
"94.177.175.13:1189",
"88.211.126.138:8080",
"187.58.215.86:8081",
"89.188.124.66:8081",
"113.86.121.40:808",
"111.23.10.42:80",
"220.249.185.178:9999",
"120.76.79.24:80",
"212.237.26.202:1189",
"45.79.99.200:80",
"5.249.144.10:1189",
"37.28.173.38:8081",
"183.153.26.166:808",
"182.52.137.147:8080",
"138.68.165.32:8118",
"103.35.169.153:8080",
"202.56.203.40:80",
"36.97.145.29:9999",
"200.76.251.166:3128",
"186.103.169.166:8080",
"212.237.26.194:1189",
"202.136.94.13:8080",
"91.187.110.75:8080",
"221.217.34.87:9000",
"212.237.27.251:1189",
"103.194.233.93:80",
"80.240.248.17:8080",
"77.81.230.15:1189",
"123.169.90.86:808",
"86.125.235.175:8080",
"88.191.174.188:80",
"200.105.148.74:3128",
"121.232.147.20:9000",
"117.211.10.148:8080",
"104.198.1.133:8080",
"125.71.245.238:8998",
"177.220.174.130:8080",
"176.237.175.231:8080",
"182.253.191.106:8080",
"113.12.214.236:8998",
"113.122.106.243:9000",
"118.255.29.32:8998",
"103.194.233.237:8080",
"103.234.254.164:80",
"80.240.100.17:8000",
"110.36.225.254:8080",
"188.38.13.209:8080",
"177.128.224.15:8080",
"97.72.106.150:87",
"217.146.214.46:8080",
"123.231.250.10:3128",
"110.138.45.185:8080",
"59.62.126.42:808",
"131.255.82.189:8080",
"36.249.25.26:808",
"36.79.65.120:8080",
"182.37.20.62:808",
"222.185.91.110:808",
"160.202.42.106:8080",
"181.115.241.90:80",
"121.232.146.135:9000",
"212.237.25.63:1189",
"187.84.222.153:80",
"140.0.123.34:8888",
"117.143.109.171:80",
"114.99.10.139:808",
"190.157.89.129:8080",
"89.36.215.132:1189",
"123.169.39.202:808",
"116.202.123.3:8080",
"103.78.11.74:80",
"112.109.95.26:8080",
"212.237.27.193:1189",
"121.232.146.244:9000",
"84.242.139.69:3128",
"212.237.25.214:1189",
"36.66.170.127:3128",
"121.52.157.200:8080",
"111.72.114.114:808",
"94.177.171.119:1189",
"49.88.192.109:808",
"103.85.162.26:8080",
"138.68.178.189:8118",
"188.213.165.250:1189",
"103.217.104.209:8080",
"175.45.188.57:8080",
"115.124.78.54:80",
"118.242.0.107:8909",
"112.214.73.253:80",
"130.211.92.157:443",
"212.237.0.135:1189",
"182.93.241.198:8080",
"59.62.126.193:808",
"192.129.188.162:9001",
"182.244.10.153:8998",
"212.237.23.253:1189",
"94.177.171.56:1189",
"89.36.213.122:1189",
"105.30.28.74:8080",
"180.254.173.232:8080",
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


