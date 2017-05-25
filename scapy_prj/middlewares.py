# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


_IP_INDEX_ = 0
IPS = [u'https://180.119.76.79:808', u'https://120.84.229.243:9000', u'https://14.153.53.105:3128', u'https://183.45.172.112:9797', u'https://113.124.104.158:8118', u'https://101.5.105.14:8123', u'https://101.23.150.118:9999', u'https://14.211.123.26:808', u'https://183.185.1.68:9797', u'https://219.136.173.41:9797', u'https://113.66.158.112:9797', u'https://61.141.186.254:9797', u'https://27.46.39.3:9797', u'https://101.23.150.110:9999', u'https://124.16.88.129:1080', u'https://153.3.101.242:1080', u'https://27.46.38.168:9797', u'https://112.95.204.132:8888', u'https://59.50.60.52:9797', u'https://111.127.232.215:8080', u'https://101.5.109.106:8123', u'https://115.200.162.239:8123', u'https://119.136.196.60:9797', u'https://219.136.175.142:9797', u'https://60.27.240.145:9999', u'https://171.37.169.156:9797', u'https://221.217.41.13:9000', u'https://115.46.73.113:8123', u'https://123.188.205.59:80', u'https://60.19.157.124:8080', u'https://101.20.221.131:9000', u'https://119.114.75.123:8080', u'https://119.29.37.247:3128', u'https://61.143.60.30:8080', u'https://180.152.109.189:9797', u'https://223.15.33.121:9797', u'https://171.113.94.113:8123', u'https://36.1.128.107:808', u'https://27.46.74.53:9999', u'https://171.36.97.218:8123', u'https://1.196.161.252:9999', u'http://60.2.148.253:80', u'https://112.232.114.213:808', u'https://183.27.193.3:808', u'https://116.226.69.170:9000', u'https://119.57.117.41:8080', u'https://125.40.26.212:9797', u'https://120.9.25.146:9999', u'https://27.46.74.54:9999', u'https://113.79.74.225:9797', u'https://139.209.100.47:9999', u'https://183.39.158.2:9797', u'https://112.95.123.147:9797', u'https://120.9.16.193:9999', u'https://125.106.94.167:8123', u'https://113.65.140.113:9999', u'https://175.155.228.85:808', u'https://113.121.255.136:808', u'https://115.151.7.225:808', u'https://175.155.241.174:808', u'https://119.5.1.108:808', u'https://114.230.106.41:808', u'https://175.155.247.122:808', u'https://175.155.244.102:808', u'https://117.57.90.133:808', u'https://182.38.111.90:808', u'https://175.155.143.233:808', u'https://116.28.110.176:808', u'https://116.28.105.202:808', u'https://113.121.181.152:808', u'https://113.206.243.151:8118', u'https://119.7.83.188:808', u'https://183.184.60.243:8080', u'https://175.155.245.201:808', u'https://114.106.20.58:808', u'https://171.38.176.135:8123', u'https://114.239.145.186:808', u'https://220.160.10.163:808', u'https://113.70.149.146:808', u'https://121.61.106.160:808', u'https://222.185.151.198:808', u'https://180.114.143.253:808', u'https://115.203.82.15:808', u'https://123.55.184.132:808', u'https://140.224.76.202:45153', u'https://114.239.1.127:808', u'https://115.220.144.159:808', u'https://125.81.107.59:8123', u'https://121.231.144.30:808', u'https://114.239.147.158:808', u'https://182.88.26.98:8123', u'https://115.202.179.119:808', u'https://182.44.254.22:808', u'https://115.202.167.189:808', u'https://123.163.165.120:808', u'https://119.7.79.21:808', u'https://114.239.151.178:808', u'https://106.3.94.134:808', u'https://121.61.97.228:808', u'https://180.118.240.190:808', u'https://113.121.40.123:808', u'http://119.5.0.102:808', u'https://175.155.246.21:808', u'https://221.229.47.70:808', u'https://117.43.0.157:808', u'https://117.88.83.102:808', u'https://125.92.33.171:808', u'https://123.55.184.151:808', u'https://113.234.167.130:8118', u'https://175.155.246.76:808', u'https://171.38.241.165:8123', u'https://116.28.109.0:808', u'https://123.55.179.172:808', u'https://115.215.70.234:808', u'https://180.118.241.124:808', u'https://115.192.67.165:808', u'https://220.160.10.176:808', u'https://115.202.181.184:808', u'https://59.62.126.78:808', u'https://123.169.35.29:808', u'https://115.202.184.57:808', u'https://112.85.110.106:808', u'https://123.55.190.71:808', u'https://115.220.5.149:808', u'https://112.84.1.119:808', u'https://115.220.3.116:808', u'https://60.178.84.150:808', u'https://183.153.1.196:808', u'https://175.155.247.6:808', u'https://114.231.241.62:808', u'https://183.153.24.174:808', u'https://125.89.121.127:808', u'https://222.94.146.66:808', u'https://183.128.179.29:808', u'http://115.213.201.71:808', u'https://117.43.0.200:808', u'https://115.220.4.79:808', u'https://60.178.87.69:808', u'https://115.212.58.154:808']

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
        print("use %s proxy ip: %s" % (_IP_INDEX_, IPS[_IP_INDEX_]))
        request.meta['proxy'] = IPS[_IP_INDEX_]
        _IP_INDEX_ = (_IP_INDEX_+1) % len(IPS)


