#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyquery import PyQuery


class parse_by_query:
    def __init__(self, content_):
        self.query = PyQuery(content_)

    def query(self, query_, type_='HTML'):
        if type_.upper() == 'TEXT':
            return self.res_text(self.query(query_))
        elif type_.upper() == 'HTML':
            return self.res_html(self.query(query_))

    def res_text(self, content_):
        return content_.text()

    def res_html(self, content_):
        return content_.html()