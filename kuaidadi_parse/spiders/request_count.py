# -*- coding: utf-8 -*-
import scrapy
import cjson
import re
from kuaidadi_parse import settings


class RequestCountSpider(scrapy.Spider):
    name = "request_count"
    allowed_domains = ["v.kuaidadi.com"]

    start_urls = tuple(["http://v.kuaidadi.com/point?cityId=%s&scope=city&date=%s&dimension=%s&num=300" % (city[0], day, dimension)
            for city in settings.CITY_MATCHING.items()
            for day in settings.DAYS
            for dimension in settings.DIMENSIONS])

    def parse(self, response):
        body = cjson.decode(response.body)
        data = body["result"]["data"]
        cityId = re.findall(r"cityId=(\d+)", response.url)[0]
        day = re.findall(r"date=(\d+)", response.url)[0]
        dimension = re.findall(r"dimension=(\w+)", response.url)[0]
        print settings.CITY_MATCHING[cityId], day, dimension
        with open("%s_DAY%s_%s" % (settings.CITY_MATCHING[cityId], day, dimension), "wb") as f:
            for t in range(24):
                _sum = 0
                for elem in data[t]:
                    _sum = _sum + elem[3]
                f.write("%s - %s: %s\n" % (t, t+1, _sum))

                
