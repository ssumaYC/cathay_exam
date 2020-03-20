# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from spider_home.settings import MONGO_HOST, MONGO_DB


class SpiderHomePipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def open_spider(self, spider):
        self.mc = MongoClient(MONGO_HOST)
        self.db = self.mc[MONGO_DB]

    def close_spider(self, spider):
        self.mc.close()


class RentingHouseMongoPipeline(MongoPipeline):
    collection = "renting_house"
    must_have_field = {"post_id", "poster_title", "poster_identity",
                       "poster_gender", "tel", "house_type",
                       "room_type", "gender_acception",
                       "house_description"}

    def process_item(self, item, spider):
        self.validate_item(item)
        self.db[self.collection].update(
            {"post_id": item["post_id"]},
            item,
            upsert=True)
        return item

    def validate_item(self, item):
        check_result, missing_fields = self.check_fields(item)
        if check_result is not True:
            raise DropItem(f"missing fields {missing_fields}")
        else:
            pass

    def check_fields(self, item):
        exists_fields = set(item)
        missing_fields = self.must_have_field - exists_fields
        return len(missing_fields) == 0, missing_fields
