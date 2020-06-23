# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from urllib.parse import urlparse
import re

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"')
browser = webdriver.Chrome(options=chrome_options)

# 解析out_url
from_urls = [
    'http://www.picodi.com/ua/hotline',
    'http://www.picodi.com/ua/iherb',
    'http://www.picodi.com/ua/inbus',
    'http://www.picodi.com/ua/infoshina',
    'http://www.picodi.com/ua/intertop',
    'http://www.picodi.com/ua/kapsula',
    'http://www.picodi.com/ua/karabas',
    'http://www.picodi.com/ua/kfc',
    'http://www.picodi.com/ua/kontramarka',
    'http://www.picodi.com/ua/lamoda',
    'http://www.picodi.com/ua/modoza',
    'http://www.picodi.com/ua/mothercare',
    'http://www.picodi.com/ua/myprotein',
    'http://www.picodi.com/ua/next',
    'http://www.picodi.com/ua/nordvpn',
    'http://www.picodi.com/ua/oshkosh',
    'http://www.picodi.com/ua/pampik',
    'http://www.picodi.com/ua/panama',
    'http://www.picodi.com/ua/raketa',
    'http://www.picodi.com/ua/red',
    'http://www.picodi.com/ua/rezina',
    'http://www.picodi.com/ua/rozetka',
    'http://www.picodi.com/ua/s-tell',
    'http://www.picodi.com/ua/shein',
    'http://www.picodi.com/ua/sl-ira',
    'http://www.picodi.com/ua/soundmag',
    'http://www.picodi.com/ua/sportsterritory',
    'http://www.picodi.com/ua/surfshark',
    'http://www.picodi.com/ua/terrasport',
    'http://www.picodi.com/ua/tickethunt',
    'http://www.picodi.com/ua/topcredit',
    'http://www.picodi.com/ua/touch',
    'http://www.picodi.com/ua/ttt',
    'http://www.picodi.com/ua/uklon',
    'http://www.picodi.com/ua/ultracash',
    'http://www.picodi.com/ua/ultra-shop',
    'http://www.picodi.com/ua/velikiua',
    'http://www.picodi.com/ua/verocash',
    'http://www.picodi.com/ua/wmarket',
    'http://www.picodi.com/ua/worldofwarships',
    'http://www.picodi.com/ua/yakaboo',
    'http://www.picodi.com/ua/yoox',
    'http://www.picodi.com/ua/zakupka',
    'http://www.picodi.com/ua/zara',
    'http://www.picodi.com/ua/zlato',
    'http://www.picodi.com/ua/avtozvuk',
    'http://www.picodi.com/ua/autoklad',
    'http://www.picodi.com/ua/globalcredit',
    'http://www.picodi.com/ua/groshik',
    'http://www.picodi.com/ua/groshivsim',
    'http://www.picodi.com/ua/e-groshi',
    'http://www.picodi.com/ua/flyuia',
    'http://www.picodi.com/ua/mgroshi',
    'http://www.picodi.com/ua/oniks',
    'http://www.picodi.com/ua/portativ',
    'http://www.picodi.com/ua/tehnoskarb',
    'http://www.picodi.com/ua/tolstosum',
    'http://www.picodi.com/ua/foxtrot',
    'http://www.picodi.com/ua/furshet',
    'http://www.picodi.com/ua/mirtrik',
    'http://www.picodi.com/ua/yaponahata',
    'http://www.picodi.com/by/pzz',
    'http://www.picodi.com/by/pizzatempo',
    'http://www.picodi.com/kz/airbnb',
    'http://www.picodi.com/kz/aliexpress',
    'http://www.picodi.com/kz/asos',
    'http://www.picodi.com/kz/aviata',
    'http://www.picodi.com/kz/banggood',
    'http://www.picodi.com/kz/chocomart',
    'http://www.picodi.com/kz/flip',
    'http://www.picodi.com/kz/fora',
    'http://www.picodi.com/kz/gearbest',
    'http://www.picodi.com/kz/gofingo',
    'http://www.picodi.com/kz/homecredit',
    'http://www.picodi.com/kz/huggies',
    'http://www.picodi.com/kz/kupivip',
    'http://www.picodi.com/kz/lelo',
    'http://www.picodi.com/kz/lingualeo',
    'http://www.picodi.com/kz/marwin',
    'http://www.picodi.com/kz/megogo',
    'http://www.picodi.com/kz/satu',
    'http://www.picodi.com/kz/shein',
    'http://www.picodi.com/kz/sulpak',
    'http://www.picodi.com/kz/taximaxim',
    'http://www.picodi.com/kz/technodom',
    'http://www.picodi.com/kz/worldoftanks',
    'http://www.picodi.com/kz/worldofwarships',
    'http://www.picodi.com/kz/yves-rocher',
    'http://www.picodi.com/kz/zaka-zaka',
    'http://www.picodi.com/kz/alfabank',
    'http://www.picodi.com/kz/shop-kz',
    'http://www.picodi.com/kz/biosfera',
    'http://www.picodi.com/kz/zaimer',
    'http://www.picodi.com/kz/kredit24',
    'http://www.picodi.com/kz/litnet',
    'http://www.picodi.com/kz/meloman',
    'http://www.picodi.com/kz/mechta',
    'http://www.picodi.com/kz/netology',
    'http://www.picodi.com/kz/sushi-master',
    'http://www.picodi.com/kz/ticketon',
    'http://www.picodi.com/kz/foxford',
    'http://www.picodi.com/kz/4slovo'
]

f = open('./2.html', 'a')

pattern = re.compile(r'<li class="link"><i class="icon icon-fa-link"></i><a href="([\s\S]*?)" target="_blank" rel="nofollow">', re.I)

out_urls = {}
for url in from_urls:
    browser.get(url)
    content = browser.page_source
    res = pattern.findall(content)
    if len(res) > 0:
        domain = urlparse(res[0]).netloc.replace('www.', '')
        sql = 'update sc_urls_merchant_domain set merchant_domain = \'' + domain + '\' where domain = \'www.picodi.com\' and url = \'' + url + '\' and merchant_domain = \'\';\n'
        print(sql)
        f.write(sql)
    sleep(20)

# 关闭文件
f.close()
# 关闭浏览器
browser.close()
