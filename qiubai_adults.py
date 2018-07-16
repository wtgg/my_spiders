import os
import time

import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
    'Referer': 'http://www.qiubaichengren.net/gif/',
}


url_get = 'http://www.qiubaichengren.net/gif/list_{}.html'

s_page = input('请输入起始页码： ')
e_page = input('请输入结束页码： ')

# 创建会话
s = requests.Session()

for i in range(int(s_page), int(e_page)+1):
    # 补全url
    url = url_get.format(i)
    # 获取每一页的源码
    r = s.get(url, headers=headers)
    r.encoding = 'gb2312'
    content = r.text
    tree = etree.HTML(content)

    # 获取每页的所有图片div
    img_div_list = tree.xpath('//div[@class="mala-text"]')
    print('开始下载第%d页图片' % i)
    for div in img_div_list:
        # 获取图片标题
        title = str(div.xpath('./div[@class="mtitle"]/a/text()')[0])
        # 获取本页图片的src
        src = str(div.xpath('.//img/@src')[0])
        dir = './糗百图片'
        if not os.path.exists(dir):
            os.mkdir(dir)

        suffix = src.split('.')[-1]
        # filename = 'page_' + str(i) + title + '.' + suffix
        filename = title + '.' + suffix
        filepath = os.path.join(dir, filename)
        try:
            # 下载图片
            data = s.get(src, headers=headers).content
            with open(filepath, 'wb') as f:
                f.write(data)
                # time.sleep(0.5)
                print('%s 下载完成' % filename)
        except Exception as e:
            print(e)

print('下载完毕')