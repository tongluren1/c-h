# -*- coding: utf-8
import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
import re
from jianshu_config import pattern_model

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import db

# # 关闭当前文件进程
# os.system("ps -ef|grep "+__file__+"|awk '{print $2}'|xargs kill -9")
# # 关闭当 chrome 进程
# os.system("ps -ef|grep chrome|awk '{print $2}'|xargs kill -9")

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)

box_pattern = pattern_model['user_list']['box_pattern']
des_pattern = pattern_model['user_list']['des_pattern']

error_num = 0
print('starttime:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def spider(url, db):
    global error_num

    browser.get(url)
    html = browser.page_source

    if len(html) > 20000:
        box = re.compile(box_pattern, re.I).findall(html)
        for box_item in box:
            UserId = re.compile(des_pattern['UserId'], re.I).findall(box_item)
            NickName = re.compile(des_pattern['NickName'], re.I).findall(box_item)
            Sex = re.compile(des_pattern['Sex'], re.I).findall(box_item)
            HomeUrl = re.compile(des_pattern['HomeUrl'], re.I).findall(box_item)
            Avatar = re.compile(des_pattern['Avatar'], re.I).findall(box_item)
            Aaying = re.compile(des_pattern['Aaying'], re.I).findall(box_item)
            RecentUpdate = re.compile(des_pattern['RecentUpdate'], re.I).findall(box_item)

            tmp_list = {}
            if len(UserId) == 0 or UserId[0].isspace() == True:
                continue
            if len(NickName) == 0 or NickName[0].isspace() == True:
                continue

            tmp_list['UserId'] = UserId[0]
            tmp_list['NickName'] = db.self_escape_string(NickName[0])

            if len(Sex) > 0:
                tmp_list['Sex'] = Sex[0]
            if len(HomeUrl) > 0:
                tmp_list['HomeUrl'] = HomeUrl[0]
            if len(Avatar) > 0:
                tmp_list['Avatar'] = Avatar[0]
            if len(Aaying) > 0:
                tmp_list['Aaying'] = db.self_escape_string(Aaying[0])

            tmp_list['RecentUpdate'] = ''
            if len(RecentUpdate) > 0:
                tmp_ = []
                for Recent in RecentUpdate:
                    tmp_.append('{"' + Recent[0] + '":"' + db.self_escape_string(Recent[1]) + '"}')
                tmp_list['RecentUpdate'] = ','.join(tmp_)
                tmp_list['RecentUpdate'] = '[' + tmp_list['RecentUpdate'] + ']'
                tmp_list['RecentUpdate'] = db.self_escape_string(tmp_list['RecentUpdate'])

            tmp_list['AddTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            tmp_list['UpdateTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            colnum_str = ','.join(tmp_list.keys())
            value_str = "','".join(tmp_list.values())
            value_str = "'" + value_str + "'"
            sql = "insert into jianshu_user (%s) values (%s) on duplicate key update NickName = '%s', RecentUpdate = '%s'; " % (
                colnum_str, value_str, tmp_list['NickName'], tmp_list['RecentUpdate'])
            try:
                db.get_row(sql)
            except BaseException:
                print('------------- error ------------')
                print(sql.encode('utf-8'))
                print('------------- error ------------')
            else:
                pass
                # print(sql.encode('utf-8'))
        sleep(1)
        error_num = 0
    else:
        if error_num > 5:
            return False
        error_num = error_num + 1
    return True


urls = []
page = 1
url = 'https://www.jianshu.com/recommendations/users?page={}'

while page <= 200:
    print('-------------------- page --------------------')
    print('-------------------- ' + str(page) + ' --------------------')
    print('-------------------- page --------------------')
    page_url = url.format(page)
    flag = spider(page_url, db())
    if flag:
        pass
    else:
        break
    page = page + 1

browser.quit()
print('endtime:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
