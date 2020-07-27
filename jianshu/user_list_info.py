import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
import re

sys.path.append('..')
from lib.db import db

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)

box_pattern = '(<div class="info">\s*?<ul>\s*?[\s\S]*?\s*?</ul>\s*?</div>\s*?</div>)'
intro_pattern = '<div class="js-intro">([\s\S]*?)</div>'
des_pattern = '<p>(\S+?)</p>'

base_url = 'https://www.jianshu.com'


def spider(url, db, user):
    browser.get(url)
    html = browser.page_source

    if len(html) > 20000:
        box = re.compile(box_pattern, re.I).findall(html)
        intro = re.compile(intro_pattern, re.I).findall(html)
        for box_item in box:
            num_list = re.compile(des_pattern, re.I).findall(box_item)
            print(num_list)

            tmp_list = {}
            tmp_list['UserId'] = user['UserId']
            tmp_list['FocusNum'] = num_list[0]
            tmp_list['FansNum'] = num_list[1]
            tmp_list['ArticleNum'] = num_list[2]
            tmp_list['WordsNum'] = num_list[3]
            tmp_list['LikeNum'] = num_list[4]
            tmp_list['Assets'] = num_list[5]

            if len(intro) > 0:
                tmp_list['Aaying'] = intro[0].replace('"', '\'')
                tmp_list['Aaying'] = tmp_list['Aaying'].replace("'", '\"')

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
                print(sql)
                print('------------- error ------------')
            else:
                print(sql)
        sleep(5)
    return True


urls = []


def getUserList(db):
    sql = "select UserId, HomeUrl from jianshu_user order by ID desc;"
    return db.get_rows(sql)


user_list = getUserList(db())
for item in user_list:
    url = base_url + item['HomeUrl']
    flag = spider(url, db(), item)
    if flag:
        print(item['UserId']+'succ')
