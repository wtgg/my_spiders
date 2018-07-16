import requests
from lxml import etree
import urllib.request
import urllib.parse
import time
import os

Config = {
    'url': 'http://www.meizitu.com/a/more_{}.html',
    'start_page': input('请输入起始页码:'),
    'end_page': input('请输入结束页码:'),

}


class MeiZiSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Referer': 'http://www.meizitu.com'
        }
        self.url = Config['url']

    def run(self):
        for page in range(int(Config['start_page']), int(Config['end_page']) + 1):
            # 构建每个页面的请求
            request = self.handle_request(page)
            # 获取每个页面的内容
            content = urllib.request.urlopen(request).read().decode('gbk')
            # 解析，处理每个页面
            self.parse_content(content)

    def handle_request(self, page):
        url = Config['url'].format(page)
        return urllib.request.Request(url=url, headers=self.headers)

    def parse_content(self, content):
        # 使用xpath,先定义一个tree对象
        tree = etree.HTML(content)
        a_pic_list = tree.xpath('//li[@class="wp-item"]/div[@class="con"]/div[@class="pic"]/a')
        # 打开图片专辑链接，进入专辑页面
        # print(pic_href_list)
        for a in a_pic_list:
            global album_name
            album_name = str(a.xpath('./img/@alt')[0]).strip('</b>')
            global album_cover
            album_cover = str(a.xpath('./img/@src')[0])
            album_href = str(a.xpath('./@href')[0])
            album_page = self.open_url(album_href)
            album_page_tree = etree.HTML(album_page)
            album_page_img_src_list = album_page_tree.xpath('//div[@id="picture"]/p/img/@src')
            # exit()
            print('开始下载：%s 专辑……' % album_name)
            for src in album_page_img_src_list:
                self.download_img(src)
            print('%s 专辑 下载完毕' % album_name)

    def open_url(self, url):
        # 构建请求对象
        request = urllib.request.Request(url=url, headers=self.headers)
        # 获取请求页面内容
        content = urllib.request.urlopen(request).read().decode('gbk')
        return content

    def download_img(self, src):
        # 下载图片存放的文件夹名字即图片专辑名
        if not os.path.exists(album_name):
            os.mkdir(album_name)
        file_name = src.split('/')[-1]
        # 文件全路径
        filepath = os.path.join(album_name, file_name)
        print('正在下载：%s' % file_name)
        # # 下载图片
        try:
            r = requests.get(src, headers=self.headers)
            with open(filepath, 'wb') as fp:
                fp.write(r.content)
        except Exception as e:
            print(e)
        # print('%s 下载完成' % file_name)
        # time.sleep(1)


def main():
    spider = MeiZiSpider()
    spider.run()


if __name__ == '__main__':
    main()
