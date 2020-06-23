#!/usr/bin/python
# -*- coding: utf-8 -*-

from news_config import Config
import sys
sys.path.append('..')
from lib.crawler import crawler
from lib.db import db
from lib.parse_by_query import parse_by_query

configObj = Config()
config = configObj.getConfig()

f = open('../log/1.txt', 'w', encoding='utf-8')

# test crawler
crawler = crawler('GET')
url_list = config['toutiao']
for item in url_list:
    response = crawler.request_url(url_list[item])
    query = parse_by_query(response.content.decode('utf-8'))
    f.write(response.content.decode('utf-8'))
    data = query.query("html .wcommonFeed")
    print(data)

# test db
# db = db()
# data = db.get_value('select `domain` from merchant_domain limit 10;')

# print(config)
