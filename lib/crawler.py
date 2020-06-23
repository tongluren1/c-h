#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests


class crawler:

    def __init__(self, type_, header_={}):
        header_['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'
        self.type_ = type_.upper()
        self.header_ = header_

    def request_url(self, url_, data_={}):
        if self.type_ == 'GET':
            response = requests.get(url_, self.header_)
        elif self.type_ == 'POST':
            response = requests.post(url_, data_, self.header_)
        return response

