# -*- coding:utf-8 -*-

import scrapy
import re, time
import random
import zlib
import bson.binary
from datetime import datetime

from pymongo import MongoClient
connection=MongoClient('localhost',27017) 

#选择myblog库  
db=connection.scapy_baike  

# 使用users集合  
urls_collection=db.urls
content_page_collection=db.content_page

__READY_FOR_SPIDER__ = []
__URL_PREFIX__ = 'https://baike.baidu.com'
__URL_PREFIX_LEN__ = len(__URL_PREFIX__) + 3
__BAIKE_DOMAIN__ = 'baike.baidu.com'
file_suffix = [
    '.css',
    '.js',
    '.svg',
    '.png',
    '.jpg'
]

class BaikeSpider(scrapy.Spider):
    name = "baike"

    def __init__(self, *args, **kwargs):
        super(BaikeSpider, self).__init__(*args, **kwargs)
        self._on_crawl_urls_ = []

    def start_requests(self):
        urls = [
            # 'https://baike.baidu.com/',
            r'https://baike.baidu.com/tashuo/browse/content?id=f78312c88b49b6e8f9fbf95f'
        ]
        data = urls_collection.find_one({'used': False})
        if data:
            self.log("first url %s" % data['url'])
            urls_collection.update(
                data,
                {'used': True, 'updated_at': datetime.now(),'url':data['url'], 'created_at': data['created_at']},
                upsert = False
            )
            self._on_crawl_urls_.append(data['url'])
            req = scrapy.Request(url=data['url'] , callback=self.parse)
            req.meta["url_data"] = data
            yield req
            # yield scrapy.Request(url=data['url'] , callback=self.parse)
        else:
            self.log("first url %s" % ('https://baike.baidu.com/'))
            urls_collection.insert({
                'url': 'https://baike.baidu.com/',
                'used': True,
                'created_at': datetime.now()
            })
            yield scrapy.Request(url='https://baike.baidu.com/' , callback=self.parse)
        lastTime = datetime.now()
        while 1:
            self.log("cost time: %s" % (datetime.now()-lastTime))
            lastTime = datetime.now()
            sleep_time = 3 + (int(random.random() * 10) % 4)
            self.log("begin  query at %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            data = urls_collection.find_one({'used': False, 'url':{'$nin':self._on_crawl_urls_}})
            self.log("finish query at %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.log("get next: %s" % data)
            if data:
                # self.log("after %ss next url %s" % (sleep_time, data['url']))
                self.log("next url %s" % (data['url']))
                # time.sleep(sleep_time)
                # urls_collection.update(
                #     data,
                #     {'used': True, 'updated_at': datetime.now(),'url':data['url'], 'created_at': data['created_at']},
                #     upsert = False
                # )
                while len(self._on_crawl_urls_) > 100:
                    del self._on_crawl_urls_[0]
                self._on_crawl_urls_.append(data['url'])
                req = scrapy.Request(url=data['url'] , callback=self.parse)
                req.meta["url_data"] = data
                yield req
            else:
                self.log("after %s next url %s" % (sleep_time, data))
                break
                # time.sleep(sleep_time)
        # for url in urls:
        #     yield scrapy.Request(url=url , callback=self.parse)

    def parse(self, response):
        urlData = response.meta["url_data"]
        if urlData:
            if urlData['url'] in self._on_crawl_urls_:
                self._on_crawl_urls_.remove(urlData['url'])
            urls_collection.update(
                urlData,
                {'used': True, 'updated_at': datetime.now(),'url':urlData['url'], 'created_at': urlData['created_at']},
                upsert = False
            )
        self.log("body size %s, url:%s" % (len(response.body), response.url))
        data = content_page_collection.find({'url': response.url})
        if not data or data.count() == 0:
            z_body = zlib.compress(response.body)
            self.log("compress %s" % len(z_body))
            content_page_collection.insert({
                'url': response.url,
                'page_content': bson.binary.Binary(z_body),
                'created_at': datetime.now()
            })
        else:
            self.log("repeat scrapy %s" % response.url)
            return
        urls=re.findall(r'<a.*?href=.*?<\/a>', response.body, re.I|re.S|re.M)
        res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
        link_list = []
        for a_url in urls:
            link_list.extend(re.findall(res_url, a_url))
        # self.log(link_list)
        for url in link_list:
            if '#' in url:
                continue
            is_continue = False
            for suffix in file_suffix:
                if suffix in url:
                    is_continue = True
                    break
            if is_continue:
                continue
            if url[0] == '/':
                # self.log("INNNN %s" % url)
                self.__addOneChildUrl__(__URL_PREFIX__+url)
                continue
            if __BAIKE_DOMAIN__ in url[:__URL_PREFIX_LEN__]:
                # self.log("INNNN %s" % url)
                self.__addOneChildUrl__(url)
            # else:
            #     self.log("%s not in %s" % (__BAIKE_DOMAIN__, url))
            # self.log("cannot --- %s" % url)
            # self.log(type(url))
        # self.log('Saved file %s' % filename)

    def __addOneChildUrl__(self, url):
        data = urls_collection.find({'url': url})
        if not data or data.count() == 0:
            # self.log("add url:%s" % url)
            urls_collection.insert({
                'url': url,
                'used': False,
                'created_at': datetime.now()
            })

        # global __READY_FOR_SPIDER__
        # __READY_FOR_SPIDER__.append(url)
        # if len(__READY_FOR_SPIDER__) >= 10:
        #     self.__saveUrlToDB__(__READY_FOR_SPIDER__)
        # __READY_FOR_SPIDER__ = []


