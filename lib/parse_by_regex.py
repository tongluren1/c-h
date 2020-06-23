#!/usr/bin/python
# -*- coding: utf-8 -*-

import re


class parse_by_regex:
    def __init__(self, pattern_):
        self.pattern = re.compile(pattern_)

    def res(self, content_):
        match = self.pattern.match(content_)
        if match:
            # 使用Match获得分组信息
            match.group()
