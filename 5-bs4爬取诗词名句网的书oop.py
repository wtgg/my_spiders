import time
import urllib.request

from bs4 import BeautifulSoup

Config = {
    # 你要爬取的书的主页
    # 限史书典籍板块
    # 'url': 'http://www.shicimingju.com/book/yangjiajiang.html',
    'url': input('请输入您要爬取的小说的主页：'),
    # 给小说重命名，如果不填，会自动生成小说的默认名
    'book_name': None,
}


class NovelSpider(object):
    def __init__(self):
        self.url = Config['url']
        self.book_name = Config['book_name']
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        }

    def handle_request(self, url):
        return urllib.request.Request(url=url, headers=self.headers)

    def open_url(self, url):
        # 构建请求对象
        request = self.handle_request(url)
        # 获取请求页面内容
        content = urllib.request.urlopen(request).read().decode('utf8')
        return content

    def get_chapter(self, href):
        content = self.open_url(href)
        soup = BeautifulSoup(content, 'lxml')
        # 获取此章节的内容
        text = soup.find('div', class_='chapter_content').text
        return text

    def parse_content(self, content):
        # 生成soup对象
        soup = BeautifulSoup(content, 'lxml')
        # 找到所有的标题和链接
        a_title_href_list = soup.select('.book-mulu > ul > li > a')  # 注意标签之间必须有空格
        # 遍历列表，获取标题和链接
        for oa in a_title_href_list:
            # 获取标题
            title = oa.string
            href = 'http://www.shicimingju.com' + oa['href']
            # 有了标题和链接还要获取每一个链接打开后页面的内容
            text = self.get_chapter(href)
            string = title + '\n' + text + '\n'
            if Config['book_name']:
                book = Config['book_name'] + '.txt'
            else:
                book = this_book_name + '.txt'
            with open(book, 'a', encoding='utf8') as fp:
                print('开始下载%s……' % title)
                fp.write(string)
                # print('完成！')
            # time.sleep(0.1)
        print('全部完成！')

    def run(self):
        content = self.open_url(self.url)
        soup = BeautifulSoup(content, 'lxml')
        global this_book_name
        this_book_name = soup.select(".book-header > h1")[0].text.strip('《》')
        self.parse_content(content)


def main():
    spider = NovelSpider()
    spider.run()


if __name__ == '__main__':
    main()
