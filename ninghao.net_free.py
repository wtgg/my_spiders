import os
import urllib.request
from lxml import etree

Config = {
    # 课程地址 NGINX：Web 服务器
    'url': 'https://ninghao.net/course/3996',
    # Wordpress 一分钟
    'url': 'https://ninghao.net/course/873',
    # 阿里云 ECS：Linux 服务器
    'url': 'https://ninghao.net/course/1584',
    # 前端库
    'url': 'https://ninghao.net/course/2939',
}


class NinghaoSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            # 'Referer': 'https://ninghao.net/'
        }
        self.url = Config['url']

    def run(self):
        # 创建请求，为了带入headers，其实可以不带，urllib.request.urlopen()可以直接打开url.不过为了模拟浏览器请求，还是加上。以免以后被反爬
        request = urllib.request.Request(url=self.url, headers=self.headers)
        # 获取课程列表页的源代码数据
        page_code = urllib.request.urlopen(request).read().decode('utf8')
        tree = etree.HTML(page_code)
        course_name = str(tree.xpath('//div[@class="course-info"]/h1/text()')[0])
        print('开始下载%s 课程……' % course_name)
        # 获取每个视频页面的链接
        a_list = tree.xpath('//div[contains(@class,"item free")]/div/div/a')
        for index, value in enumerate(a_list):
            # 每个视频的标题
            title = str(value.xpath('./text()')[0])
            # 每个视频的链接
            href = str(value.xpath('./@href')[0])
            # 链接补充完整
            href = 'https://ninghao.net' + href
            # r = urllib.request.Request(href, self.headers)
            # 每个视频页面的源码
            video_page_code = urllib.request.urlopen(href).read().decode('utf8')
            # print(video_page_code)
            # exit()
            v_tree = etree.HTML(video_page_code)
            # 获取视频的src地址
            src = str(v_tree.xpath('//video/source/@src')[0])
            # 重命名视频，给每个视频添加上序号
            name = str(index + 1) + '__' + title
            # 视频存放文件夹
            dir_path = './' + course_name
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            # 视频后缀
            suffix = src.split('.')[-1]
            # 下载视频的文件名
            filename = name + '.' + suffix
            # 补全路径
            filepath = os.path.join(course_name, filename)
            try:
                # 使用urlretrieve方法下载视频
                print('正在下载%s……' % filename)
                urllib.request.urlretrieve(src, filepath)
            except Exception as e:
                print(e)
        print('%s 课程下载完毕' % course_name)


if __name__ == '__main__':
    spider = NinghaoSpider()
    print('开始下载……')
    spider.run()
