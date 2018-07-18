import os
import requests
from user_agents import agents
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

path = r'D:\soft\tools\chromedriver.exe'
browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

UA = random.choice(agents)
headers = {
    'User-Agent': UA,
}

url = 'http://tt.mop.com'

browser.get(url)
# time.sleep(2)
# 拖动滚动条，让图片都显示出来，并且查看网页的内容，那个src2属性有没有修改为src
js = 'document.body.scrollTop=10000'
# 循环触发js，加载瀑布流，用selenium只在这一点有体现
for i in range(2):
    browser.execute_script(js)
    time.sleep(3)

content = browser.page_source
tree = etree.HTML(content)
a_list = tree.xpath('//div[@class="box"]/a[@class="box-img"]')


def download_album(album, a_href):
    content = requests.get(a_href, headers=headers).text
    tree = etree.HTML(content)
    src_list = tree.xpath('//p[@class="tc mb10"]/img/@src')
    img_folder = './猫女郎3'
    if not os.path.exists(img_folder):
        os.mkdir(img_folder)
    folder = img_folder + '/' + album
    if not os.path.exists(folder):
        os.mkdir(folder)
    for i, src in enumerate(src_list):
        src = 'http:' + str(src)
        suffix = src.split('.')[-1].lower()
        filename = str(i + 1) + '.' + suffix
        filepath = folder + '/' + filename
        print('正在下载%s' % filename)
        # 此处需要停顿，否则只有文件夹，不会下载图片，应该是反爬检测访问频率
        n = random.uniform(1, 2)
        time.sleep(n)
        data = requests.get(url=src, headers=headers).content
        try:
            with open(filepath, 'wb') as f:
                f.write(data)
        except Exception as e:
            print(e)


for a in a_list:
    album = str(a.xpath('./h2[@class="ttbox-title"]/text()')[0])
    a_href = 'http:' + str(a.xpath('./@href')[0])
    print('开始下载%s专辑……' % album)
    download_album(album, a_href)
