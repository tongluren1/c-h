import sys

sys.path.append('..')
from lib.crawler import crawler
from lib.db import db
from lib.parse_by_query import parse_by_query
from lib.speedy import speedy
import urllib.parse

config = {
    # 'base_url': 'https://news.sina.com.cn/',
    'base_url': 'https://blog.csdn.net/ysblogs/article/details/88530124',
    'pattern': ''
}

url = config['base_url']
crawler = crawler(type_='GET')
data = crawler.request_url(url_=url)
speedy = speedy()
content = data.content.decode('utf-8')
host = urllib.parse.urlparse(data.url).hostname

speedy.print_text(data.content.decode())
