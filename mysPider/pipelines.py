# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from mysPider import settings
import os
import urllib
import json

class MyspiderPipeline(object):
    def process_item(self, item, spider):
        dir_path = '%s/%s'%(settings.DATA_STORE,spider.name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        result = {
            'name':item['name'],
            'related_drug': item['related_drug'],
            'effect' : item['effect']
        }
        # print(result)
        with open(dir_path+"/result1.txt",'a+') as file:
            file.write(json.dumps(result,indent=4,ensure_ascii=False))
            file.write("\n")
        return item
