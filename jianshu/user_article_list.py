import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
import re
from jianshu_config import pattern_model

sys.path.append('..')
from lib.db import db

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
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
            tmp_list['Title'] = tmp_list['Title'].replace('"', '\'')
            tmp_list['Title'] = tmp_list['Title'].replace("'", '\"').strip()

            if len(Abstract) > 0:
                tmp_list['Abstract'] = Abstract[0]
                tmp_list['Abstract'] = tmp_list['Abstract'].replace('"', '\'')
                tmp_list['Abstract'] = tmp_list['Abstract'].replace("'", '\"').strip()
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
                db.get_row(sql)
                error_num = 0
            except BaseException:
                print('------------- error ------------')
                print(sql)
                print('------------- error ------------')
            else:
                print(sql)
    else:
        error_num = error_num + 1

    if error_num > 0:
        return False

    sleep(8)
    return True


def getUserList(db):
    sql = "select ID, UserId, NickName, HomeUrl, IsNewUser, ArticleUpdate from jianshu_user WHERE ID NOT in (SELECT DISTINCT UID from jianshu_article_list) order by ID DESC;"
    return db.get_rows(sql)


for user in getUserList(db()):
    page = 1
    url = 'https://www.jianshu.com/u/' + user['UserId'] + '?order_by=shared_at&page={}'
    while page <= 150:
        print('-------------------- page --------------------')
        print('-------------------- ' + user['NickName'] + ' : ' + str(page) + ' --------------------')
        print('-------------------- page --------------------')
        page_url = url.format(page)
        print(page_url)
        flag = spider(page_url, db())
        if flag:
            pass
        else:
            break
        page = page + 1
