from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing.dummy import Pool

chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(options=chrome_options)


def spider(url):
    browser.get(url)
    html = browser.page_source
    f = open('./1.log', 'a', encoding='utf-8')
    f.write(html)
    f.close()


def run(x):
    url = 'https://www.jianshu.com/recommendations/users?page={}'
    pages = []
    for i in range(0, x * 10):
        page = url.format(i)
        pages.append(page)
    print(pages)
    pool = Pool(5)
    result = pool.map(spider, pages)
    pool.close()
    pool.join()
    return result


if __name__ == '__main__':
    run(1)
