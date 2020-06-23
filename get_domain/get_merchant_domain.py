# -*- coding: utf-8 -*-
import sys
from get_merchant_domain_helper import helper

# python get_merchant_domain.py www.moins-depenser.com 0
# set @t = NOW();
# SELECT CONCAT('INSERT INTO merchant_domain(DstUrl, domain, AddTime) VALUES (', '"', url, '","', domain, '","', @t, '");') FROM `sc_urls_merchant_domain` WHERE domain = 'www.savings.co.jp' AND merchant_domain = '';
# SELECT CONCAT('update sc_urls_merchant_domain set merchant_domain = "', MerchantDomain, '" where merchant_domain = "" and url = "', DstUrl, '";') FROM `merchant_domain` WHERE domain = 'www.savings.co.jp' AND MerchantDomain <> '';

if len(sys.argv) < 3:
    quit('argv error!')

domain = sys.argv[1]
type_ = sys.argv[2]

helper = helper(domain)
# 需要跳转 1
# 不需要跳转 0
helper.run(type_)
