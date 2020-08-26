# -*- coding: utf-8

import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, datetime
import json
from time import sleep
import re
from jianshu_config import pattern_model
from jianshu_config import base_url

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import db

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)

box_pattern = pattern_model['article_info']['box_pattern']

print('starttime:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def spider(url, db, article):
    browser.get(url)
    html = browser.page_source

    if len(html) > 90000:
        box = re.compile(box_pattern, re.I).findall(html)
        if len(box) > 0:
            info = json.loads(box[0])
            data = info['props']['initialState']['note']['data']

            tmp_list = {}
            status = 'DONE'
            tmp_list['UID'] = str(article['UID'])
            tmp_list['AID'] = str(article['ID'])
            tmp_list['DataJson'] = db.self_escape_string(json.dumps(data)).strip()
            tmp_list['LastUpdatedAt'] = datetime.datetime.fromtimestamp(data['last_updated_at']).strftime(
                "%Y-%m-%d %H:%M:%S")
            tmp_list['Title'] = db.self_escape_string(data['public_title']).strip()
            tmp_list['CommentsCount'] = str(data['comments_count'])
            tmp_list['Content'] = db.self_escape_string(data['free_content']).strip()
            tmp_list['LikesCount'] = str(data['likes_count'])
            tmp_list['PaidType'] = data['paid_type']
            tmp_list['Wordage'] = str(data['wordage'])
            tmp_list['FeaturedCommentsCount'] = str(data['featured_comments_count'])
            tmp_list['DownvotesCount'] = str(data['downvotes_count'])
            tmp_list['TotalRewardsCount'] = str(data['total_rewards_count'])
            tmp_list['FirstSharedAt'] = datetime.datetime.fromtimestamp(data['first_shared_at']).strftime(
                "%Y-%m-%d %H:%M:%S")
            tmp_list['ViewsCount'] = str(data['views_count'])
            tmp_list['NotebookId'] = str(data['notebook_id'])
            tmp_list['AddTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            tmp_list['UpdateTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            column_str = ','.join(tmp_list.keys())
            value_str = "','".join(tmp_list.values())
            value_str = "'" + value_str + "'"
            sql = "insert into jianshu_article_info (%s) values (%s)" % (column_str, value_str)
            try:
                db.db_reconnect()
                db.query(sql)
            except BaseException:
                status = 'FAILED'
                print('------------- error ------------')
                print(sql.encode('utf-8'))
                print('------------- error ------------')
            else:
                pass

            sql = "update jianshu_article_list set Status = '%s' where ArticleID = '%s'" % (
                status, article['ArticleID'])
            db.db_reconnect()
            db.query(sql)
    sleep(8)


def getArticleList(db, page):
    sql = "select ID, UID, ArticleID, Title from jianshu_article_list where Status in ('NEW', 'RECENT_UPDATE') order by ID desc limit " + str(
        page) + ", 1000;"
    return db.get_rows(sql)


for page in range(1000):
    article_list = getArticleList(db(), page)

    if len(article_list) < 1:
        break
    for article in article_list:
        url = base_url + 'p/' + article['ArticleID']
        spider(url, db(), article)

browser.quit()
print('endtime:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
