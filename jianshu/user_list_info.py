# -*- coding: utf-8
import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import db
from jianshu_config import pattern_model
import time

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)

box_pattern = pattern_model['user_list_info']['box_pattern']
intro_pattern = pattern_model['user_list_info']['intro_pattern']
des_pattern = pattern_model['user_list_info']['des_pattern']

base_url = 'https://www.jianshu.com'

print('starttime:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def spider(url, db, user):
    browser.get(url)
    html = browser.page_source

    if len(html) > 6000:
        box = re.compile(box_pattern, re.I).findall(html)
        intro = re.compile(intro_pattern, re.I).findall(html)
        for box_item in box:
            num_list = re.compile(des_pattern, re.I).findall(box_item)

            tmp_list = {}
            tmp_list['UserId'] = user['UserId']
            if len(num_list) > 0:
                tmp_list['FocusNum'] = num_list[0]
            else:
                tmp_list['FocusNum'] = '0'
            if len(num_list) > 1:
                tmp_list['FansNum'] = num_list[1]
            else:
                tmp_list['FansNum'] = '0'
            if len(num_list) > 2:
                tmp_list['ArticleNum'] = num_list[2]
            else:
                tmp_list['ArticleNum'] = '0'
            if len(num_list) > 3:
                tmp_list['WordsNum'] = num_list[3]
            else:
                tmp_list['WordsNum'] = '0'
            if len(num_list) > 4:
                tmp_list['LikeNum'] = num_list[4]
            else:
                tmp_list['LikeNum'] = '0'
            if len(num_list) > 5:
                tmp_list['Assets'] = num_list[5]
            else:
                tmp_list['Assets'] = '0'

            if len(intro) > 0:
                tmp_list['Aaying'] = db.self_escape_string(intro[0]).strip('\\n').strip()

            tmp_list['UpdateTime'] = tmp_list['AddTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            colnum_str = ','.join(tmp_list.keys())
            value_str = "','".join(tmp_list.values())
            value_str = "'" + value_str + "'"
            sql = "insert into jianshu_user_info (%s) values (%s) on duplicate key update Aaying = '%s', FocusNum = '%s', FansNum = '%s', ArticleNum = '%s', WordsNum = '%s', LikeNum = '%s', Assets = '%s'; " % (
                colnum_str, value_str, tmp_list['Aaying'], tmp_list['FocusNum'], tmp_list['FansNum'],
                tmp_list['ArticleNum'],
                tmp_list['WordsNum'], tmp_list['LikeNum'], tmp_list['Assets'])
            try:
                db.get_row(sql)
            except BaseException:
                print('------------- error ------------')
                print(sql.encode('utf-8'))
                print('------------- error ------------')
            else:
                pass
                # print(sql.encode('utf-8'))
        sleep(10)
    return True


urls = []


def getUserList(db):
    # sql = "select UserId, HomeUrl from jianshu_user order by ID desc;"
    sql = "select UserId, HomeUrl from jianshu_user WHERE UserId NOT in (SELECT UserId from jianshu_user_info) order by ID desc;"
    return db.get_rows(sql)


user_list = getUserList(db())
for item in user_list:
    url = base_url + item['HomeUrl']
    flag = spider(url, db(), item)
    if flag:
        print(item['UserId'] + 'succ')


browser.quit()
print('endtime:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
