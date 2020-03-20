# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import re


class SpiderHomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class RentingHouse(scrapy.Item):

    source = scrapy.Field()
    post_id = scrapy.Field()
    poster_title = scrapy.Field()
    poster_identity = scrapy.Field()
    poster_gender = scrapy.Field()
    tel = scrapy.Field()
    house_type = scrapy.Field()
    room_type = scrapy.Field()
    gender_acception = scrapy.Field()
    house_description = scrapy.Field()
    region = scrapy.Field()


def map_title_gender(title):
    if "先生" in title:
        return "male"
    elif "小姐" in title:
        return "female"
    elif "太太" in title:
        return "female"
    elif "媽媽" in title:
        return "female"
    elif "女士" in title:
        return "female"
    else:
        return "unknow"


def map_identity(identity):
    if "屋主" in identity:
        return "owner"
    elif "仲介" in identity:
        return "broker"
    elif "代理人" in identity:
        return "agent"
    else:
        return identity


def map_gender_acception(value):
    if "皆可" in value:
        return "both"
    elif "男" in value:
        return "male"
    elif "女" in value:
        return "female"
    else:
        return "unknow"


def clean_text(text):
    t = remove_tags(text)
    t = t.replace("\xa0", "")
    t = t.strip()
    return t


def extract_value(key, text):
    regex = re.compile(f"{key}[:：](.+)")
    try:
        value = regex.search(text).group(1)
    except (IndexError, AttributeError):
        value = None
    return value


def clean_and_map_tel(tel):
    regex = re.compile(r"[ -]")
    tel = regex.sub("", tel)
    tel = tel.replace("轉", "#")
    return tel


class RHItemLoader(ItemLoader):

    default_output_processor = TakeFirst()
    poster_identity_in = MapCompose(map_identity)
    poster_gender_in = MapCompose(map_title_gender)
    tel_in = MapCompose(clean_and_map_tel)
    house_type_in = MapCompose(clean_text,
                               lambda t: extract_value("型態", t))
    room_type_in = MapCompose(clean_text,
                              lambda t: extract_value("現況", t))
    gender_acception_in = MapCompose(clean_text,
                                     lambda t: extract_value("性別要求", t),
                                     map_gender_acception)
    house_description_in = MapCompose(clean_text)
