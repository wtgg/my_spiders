import os
import requests
from lxml import etree

# 配置项
Config = {
    # 你要爬取的课程 composer视频教程
    'url': 'http://www.houdunren.com/houdunren18_lesson_49',
    # 你在本站的用户名
    'username': 'xxx',
    # 密码
    'password': 'xxx',

}


class HDphpSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            # 'Referer': 'http://www.houdunren.com', 
        }
        self.url = Config['url']

    def run(self):
        # 先模拟登录
        # 登录地址
        post_url = 'http://www.houdunren.com/?m=ucenter&action=controller/entry/login'

        # 登录表单数据
        data = {
            'csrf_token': 'f9edeb928b934f4104b5d80e2452a692',
            'username': Config['username'],
            'password': Config['password'],
        }

        # 创建一个会话
        global s
        s = requests.Session()

        s.post(url=post_url, headers=self.headers, data=data)

        # 1. 解析源页面，获取源页面源码
        content = s.get(self.url, headers=self.headers).text
        # print(content)
        # exit()
        # 2. 获取页面的课程名称及各个视频的播放链接
        tree = etree.HTML(content)

        member = str(tree.xpath('//ul[@class="dropdown-menu"]/li/a/text()'))
        # print(member)
        # exit()
        global lesson_title
        lesson_title = str(tree.xpath('//div[@class="info"]//span[@class="lesson-title"]/text()')[0])
        a_list = tree.xpath('//div[@class="row"]/ul/li/a')

        # 3. 打开各个详情页，获取每个播放页视频的src，下载视频
        for a in a_list:
            href = str(a.xpath('./@href')[0])
            # 补全href
            href = 'http://www.houdunren.com' + href
            title = str(a.xpath('./text()')[0]).strip()
            self.download(href, title)
        print('ok')

    def parse(self, url):
        content = requests.get(self.url, self.headers).text
        return content

    def download(self, href, title):
        # 获取视频播放页的源码
        page_code = s.get(url=href, headers=self.headers).text

        tree = etree.HTML(page_code)
        member = str(tree.xpath('//ul[@class="dropdown-menu"]/li/a/text()'))

        src = str(etree.HTML(page_code).xpath('//video/source/@src')[0])

        # 视频存放目录
        dir = './video'
        if not os.path.exists(dir):
            os.mkdir(dir)
        suffix = src.split('.')[-1]
        file_name = title + '.' + suffix
        filepath = os.path.join(dir, file_name)
        headers_download = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Referer': 'http://www.houdunren.com',  # 下载视频必须有Referer参数
        }
        try:
            r = s.get(src, headers=headers_download)
            print('开始下载%s……' % file_name)
            with open(filepath, 'wb') as fp:
                fp.write(r.content)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    spider = HDphpSpider()
    spider.run()
