from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing.dummy import Pool
from urllib.parse import urlparse
from time import sleep

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)
file_path = 'F:/jianshu/user_list/'


def spider(url):
    browser.get(url)
    html = browser.page_source
    f = open('./1.html', 'a', encoding='utf-8')
    f.write(html)
    f.close()

    if len(html) > 20000:
        file_name = urlparse(url).query.replace('page=', '')
        file_name = file_path + 'page_' + file_name + '.html'
        print(file_name)
        f = open(file_name, 'a', encoding='utf-8')
        f.write(html)
        f.close()
        print('url:' + url + '\n')

    # sleep(5)


urls = []
page = 1
url = 'https://www.jianshu.com/recommendations/users?page={}'
while page <= 100:
    page_url = url.format(page)
    urls.append(page_url)
    page = page + 1

pool = Pool(5)
res = pool.map(spider, urls)
pool.close()
pool.join()
