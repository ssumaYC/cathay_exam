from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext
from copy import copy
from elasticsearch import Elasticsearch
import json
import jieba


conf = SparkConf().setMaster("local").setAppName("Cathay exam")
sc = SparkContext(conf=conf)
hc = HiveContext(sc)
hc.sql("use cathay_exam")
rows_dict = hc.sql('select * from renting_house').rdd.map(lambda r: r.asDict()).collect()
es = Elasticsearch(["elasticsearch"])
for d in rows_dict:
    d['cut_description'] = list(jieba.cut(d['house_description']))
    res = es.index(index="renting_houses", id=d['post_id'], body=json.dumps(d, ensure_ascii=False))
    print(res)
