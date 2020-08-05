#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql


class db:
    def __init__(self, host_='localhost', port_=3306, user_='root', passwd_='123456', db_='crawler',
                 charset_='utf8mb4'):
        self.db = pymysql.connect(host=host_, port=port_, user=user_, passwd=passwd_, db=db_, charset=charset_,
                                  cursorclass=pymysql.cursors.DictCursor)

    def get_row(self, sql_):
        cursor = self.db.cursor()
        cursor.execute(sql_)
        data = cursor.fetchone()
        return data

    def query(self, sql_):
        cursor = self.db.cursor()
        cursor.execute(sql_)
        self.db.commit()
        cursor.close()
        self.db.close()

    def get_rows(self, sql_):
        cursor = self.db.cursor()
        cursor.execute(sql_)
        data = cursor.fetchall()
        return data

    def get_column(self, sql_, column_):
        cursor = self.db.cursor()
        cursor.execute(sql_)
        data = cursor.fetchall()
        res = []
        for item in data:
            res.append(item[column_])
        return res

    def get_value(self, sql_):
        cursor = self.db.cursor()
        cursor.execute(sql_)
        data = cursor.fetchone()
        if data is not None:
            return list(data.values())[0]

    def db_close(self):
        self.db.close()

    def db_reconnect(self):
        self.db.ping(reconnect=True)

    def self_escape_string(self, string):
        return pymysql.escape_string(value=string)
