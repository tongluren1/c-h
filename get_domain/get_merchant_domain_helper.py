# -*- coding: utf-8 -*-
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.parse import urlparse
import re


class helper:
    def __init__(self, tmp_id):
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='crawler', charset='utf8')
        self.cursor = db.cursor()
        self.tmp_id = tmp_id
        chrome_options = Options()
        # 设置chrome浏览器无界面模式
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=chrome_options)
        self.config = self.config()
        self.config['pattern'] = re.compile(self.config['pattern'], re.I)

    def config(self):
        config = {
            'www.moins-depenser.com': {
                'pattern': 'class="icon icon-2x ico-support"[\s\S]*?<a href="([\s\S]*?)" target="_blank" rel="nofollow">'
            },
            'test': {
                'pattern': 'class="icon icon-2x ico-support"[\s\S]*?<a href="([\s\S]*?)" target="_blank" rel="nofollow">'
            },
            'www.savings.co.jp': {
                'pattern': '<a data-gatrack="step0-common" href="(\S+?)" target="_blank" class="store_btn" rel="nofollow\s*?noopener">',
                'http_': 'https://www.savings.co.jp'
            }
        }
        if self.tmp_id in config.keys():
            return config[self.tmp_id]
        else:
            quit('not domain config!')

    def run(self, type_):
        sql = "select DstUrl, ID as `key` from merchant_domain where `domain` = '" + self.tmp_id + "' AND (MerchantDomain IS NULL OR MerchantDomain = '');"
        self.cursor.execute(sql)
        for item in self.cursor.fetchall():
            if type_ == 0:
                self.request_url(item)
            else:
                self.need_jump_request_url(item)

        self.browser_close()
        self.cursor_close()

    def request_url(self, item):
        tmp_url = item[0]
        row_key = item[1]

        self.browser.get(tmp_url)
        sleep(3)
        res = self.config['pattern'].findall(self.browser.page_source)
        if len(res) > 0:
            domain = urlparse(res[0]).netloc.replace('www.', '')
            self.update_row(domain, row_key)
        return

    def need_jump_request_url(self, item):
        tmp_url = item[0]
        row_key = item[1]
        self.browser.get(tmp_url)
        sleep(3)
        res = self.config['pattern'].findall(self.browser.page_source)
        if len(res) > 0:
            if 'http_' in self.config.keys():
                self.browser.get(self.config['http_'] + res[0])
            else:
                self.browser.get(res[0])
            domain = urlparse(self.browser.current_url).netloc.replace('www.', '')
            self.update_row(domain, row_key)
        return

    def update_row(self, domain, row_key):
        sql = "update merchant_domain set MerchantDomain = '" + domain + "' where ID = '" + str(row_key) + "';"
        self.cursor.execute(sql)
        return

    def cursor_close(self):
        self.cursor.close()

    def browser_close(self):
        self.browser.close()
