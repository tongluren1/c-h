# -*- coding: utf-8
import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
import re
import json
from jianshu_config import pattern_model

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.db import db

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)

error_num = 0
box_pattern = pattern_model['article_list']['box_pattern']
des_pattern = pattern_model['article_list']['des_pattern']


def spider(url, db):
    global error_num

    browser.get(url)
    html = browser.page_source

    if len(html) > 10000:
        box = re.compile(box_pattern, re.I).findall(html)
        if len(box) == 0:
            error_num = error_num + 1

        for box_item in box:
            ArticleID = re.compile(des_pattern['ArticleID'], re.I).findall(box_item)
            NoteId = re.compile(des_pattern['NoteId'], re.I).findall(box_item)
            Title = re.compile(des_pattern['Title'], re.I).findall(box_item)
            Abstract = re.compile(des_pattern['Abstract'], re.I).findall(box_item)
            Paid = re.compile(des_pattern['Paid'], re.I).findall(box_item)
            ReadNum = re.compile(des_pattern['ReadNum'], re.I).findall(box_item)
            CommentsNum = re.compile(des_pattern['CommentsNum'], re.I).findall(box_item)
            LikeNum = re.compile(des_pattern['LikeNum'], re.I).findall(box_item)
            CreateTime = re.compile(des_pattern['CreateTime'], re.I).findall(box_item)

            tmp_list = {}
            if len(ArticleID) == 0 or ArticleID[0].isspace() == True:
                continue
            if len(NoteId) == 0 or NoteId[0].isspace() == True:
                continue
            if len(Title) == 0 or Title[0].isspace() == True:
                continue

            tmp_list['ArticleID'] = ArticleID[0]
            tmp_list['NoteId'] = NoteId[0]
            tmp_list['Title'] = Title[0]
            tmp_list['Title'] = db.self_escape_string(tmp_list['Title'])

            if len(Abstract) > 0:
                tmp_list['Abstract'] = Abstract[0]
                tmp_list['Abstract'] = db.self_escape_string(tmp_list['Abstract'])
            else:
                tmp_list['Abstract'] = ''
            if len(Paid) > 0:
                tmp_list['Paid'] = Paid[0]
            else:
                tmp_list['Paid'] = '0'
            if len(ReadNum) > 0:
                tmp_list['ReadNum'] = ReadNum[0]
            else:
                tmp_list['ReadNum'] = '0'
            if len(CommentsNum) > 0:
                tmp_list['CommentsNum'] = CommentsNum[0]
            else:
                tmp_list['CommentsNum'] = '0'
            if len(LikeNum) > 0:
                tmp_list['LikeNum'] = LikeNum[0]
            else:
                tmp_list['LikeNum'] = '0'

            if len(CreateTime) == 0:
                tmp_list['CreateTime'] = '0000-00-00 00:00:00'
            else:
                if len(CreateTime[0]) > 1:
                    tmp_list['CreateTime'] = CreateTime[0][0] + ' ' + CreateTime[0][1]
                else:
                    tmp_list['CreateTime'] = '0000-00-00 00:00:00'

            tmp_list['AddTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            tmp_list['UpdateTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            tmp_list['UID'] = str(user['ID'])

            colnum_str = ','.join(tmp_list.keys())
            value_str = "','".join(tmp_list.values())
            value_str = "'" + value_str + "'"
            sql = "insert into jianshu_article_list (%s) values (%s) on duplicate key update Title = '%s',Abstract = '%s',Paid = '%s',ReadNum = '%s',CommentsNum = '%s',LikeNum = '%s'; " % (
                colnum_str, value_str, tmp_list['Title'], tmp_list['Abstract'], tmp_list['Paid'], tmp_list['ReadNum'],
                tmp_list['CommentsNum'], tmp_list['LikeNum'])
            try:
                db.query(sql)
                error_num = 0
            except BaseException:
                print('------------- error ------------')
                print(sql.encode('utf-8'))
                print('------------- error ------------')
            else:
                pass
                # print(sql.encode('utf-8'))
    else:
        error_num = error_num + 1

    if error_num > 0:
        return False

    sleep(8)
    return True


def getUserList(db):
    sql = "select ID, UserId, NickName, HomeUrl, IsNewUser, RecentUpdate from jianshu_user order by ID DESC;"
    return db.get_rows(sql)


db = db()
for user in getUserList(db):
    if user['IsNewUser'] == 'YES':
        page = 1
        url = 'https://www.jianshu.com/u/' + user['UserId'] + '?order_by=shared_at&page={}'
        while page <= 150:
            print('-------------------- page --------------------')
            print('-------------------- ' + user['NickName'].encode('utf-8') + ' : ' + str(
                page) + ' --------------------')
            print('-------------------- page --------------------')
            page_url = url.format(page)
            print(page_url)
            flag = spider(page_url, db)
            if flag:
                pass
            else:
                break
            page = page + 1

        update_sql = 'UPDATE jianshu_user SET IsNewUser = "NO" WHERE IsNewUser = "YES" AND ID = ' + str(user['ID'])
        db.query(update_sql)
        print(update_sql.encode('utf-8'))
    else:
        recent_update = user['RecentUpdate']
        recent_update = json.loads(recent_update)
        for new_article in recent_update:
            new_article_ID = list(new_article.keys())[0].replace('/p/', '')
            new_article_title = list(new_article.values())[0]
            new_article_title = db.self_escape_string(new_article_title)

            new_article_sql = "INSERT INTO jianshu_article_list (ArticleID, UID, Title, Status, AddTime, UpdateTime) VALUES	('%s', %s, '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE Title = '%s';" % (
                new_article_ID, user['ID'], new_article_title, 'RECENT_UPDATE',
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), new_article_title)
            db.db_reconnect()
            db.query(new_article_sql)
            print(new_article_sql.encode('utf-8'))

browser.quit()
