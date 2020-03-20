# -*- coding: utf-8 -*-
import scrapy
from spider_home.items import RentingHouse, RHItemLoader
from spider_home import toolbox as tb
import json
import math
from urllib.parse import urlparse, parse_qs


class A591RentingHouseSpider(scrapy.Spider):
    name = '591_renting_house'
    allowed_domains = ['591.com.tw']
    start_urls = [
        'https://rent.591.com.tw/?kind=0&region=1',
        'https://rent.591.com.tw/?kind=0&region=3'
    ]
    api_url = "https://rent.591.com.tw/home/search/rsList?"\
        "is_new_list=1&type=1&kind=0&searchtype=1&"\
        "region={}&firstRow={}"
    custom_settings = {
        'ITEM_PIPELINES': {
            'spider_home.pipelines.RentingHouseMongoPipeline': 300,
        }
    }

    def parse(self, response):
        qs = parse_qs(urlparse(response.url).query)
        region_code = qs['region'][0]
        cookie_dict = tb.extract_ck2dict(response)
        cookie_dict['urlJumpIp'] = region_code
        self.csrf_token = response\
            .xpath('//head/meta[@name="csrf-token"]/@content')\
            .get()
        yield scrapy.http.Request(self.api_url.format(region_code, "0"),
                                  callback=self.extract_pages,
                                  headers={
                                      'X-CSRF-TOKEN': self.csrf_token
                                  },
                                  cookies=cookie_dict,
                                  dont_filter=True)
        yield scrapy.http.Request(self.api_url.format(region_code, "0"),
                                  callback=self.extract_item_ids,
                                  headers={
                                      'X-CSRF-TOKEN': self.csrf_token
                                  },
                                  cookies=cookie_dict,
                                  dont_filter=True)

    def extract_pages(self, response):
        qs = parse_qs(urlparse(response.url).query)
        rc = qs['region'][0]
        cookie_dict = tb.extract_ck2dict(response)
        cookie_dict['urlJumpIp'] = rc
        data = json.loads(response.text)
        num_items = int(data['records'].replace(",", ""))
        num_pages = math.ceil(num_items // 30)
        for page in range(2, num_pages + 1):
            first_row = (page - 1) * 30
            yield scrapy.http.Request(self.api_url.format(rc, first_row),
                                      callback=self.extract_item_ids,
                                      headers={
                                          'X-CSRF-TOKEN': self.csrf_token
                                      },
                                      cookies=cookie_dict,
                                      dont_filter=True)

    def extract_item_ids(self, response):
        data = json.loads(response.text)
        for d in data['data']['data']:
            item_id = d['id']
            url = f"https://rent.591.com.tw/rent-detail-{item_id}.html"
            yield scrapy.http.Request(url,
                                      callback=self.parse_item,
                                      meta={'item_id': str(item_id)})

    def parse_item(self, response):
        loader = RHItemLoader(item=RentingHouse(), response=response)
        loader.add_value("source", "591")
        loader.add_value("post_id", response.meta['item_id'])
        user_info_loader = loader.nested_css("div.userInfo")
        poster_title_css = "span.kfCallName::attr(data-name)"
        user_info_loader.add_css("poster_title", poster_title_css)
        user_info_loader.add_css("poster_gender", poster_title_css)
        user_info_loader.add_xpath("poster_identity", "div/div/div/text()")
        user_info_loader.add_css("tel", "span.dialPhoneNum::attr(data-value)")
        user_info_loader.add_css("tel", "div.hidtel::text")
        house_info_css = "div.detailInfo ul.attr li"
        loader.add_css("house_type", house_info_css)
        loader.add_css("room_type", house_info_css)
        loader.add_css("gender_acception", "ul.labelList li")
        loader.add_css("house_description", "div.houseIntro")
        loader.add_xpath("region", "//div[@id='propNav']/a[3]/text()")
        item = loader.load_item()
        return item
