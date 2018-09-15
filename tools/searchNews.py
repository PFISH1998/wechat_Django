import requests
import re
from bs4 import BeautifulSoup


class GetNews:

    def __init__(self, url):
        self.url = url

    def get_html(self):
        r = requests.get(self.url)
        r.encoding = 'UTF-8'
        return r.text

    def get_page(self, html):
        print(html)
        news_list = []
        for news in re.compile(r'.*?<tr(.*?)</tr>.*?').findall(html)[5:-1]:
            # print(news)

            # 新闻标题，链接
            for result in re.compile(r'.*?href=\'(.*?).html\'.*?title=\'(.*?)\'').findall(news):
                title = result[1]
                url = 'http://www.cidp.edu.cn' + result[0] + '.html'
                try:
                    print('get:', title, url)
                    page_content, pub_time = self.get_news_content(url)
                except requests.exceptions:
                    continue

                news_list.append({'url': url, 'title': title, 'page_content': page_content, 'pub_time': pub_time})
        print(news_list)
        return news_list

    @ staticmethod
    def get_news_content(url):
        page = requests.get(url)
        page.encoding = 'UTF-8'
        html = page.text
        public_time = re.compile(r'.*?<meta name="PubDate" content="(.*?)">').findall(html)
        soup = BeautifulSoup(html, 'lxml')
        page_list = []
        for p in soup.find_all('p'):
            str = ''
            # print(p)
            # 拿到 a 标签里的图片链接
            # print(str.join(p.stripped_strings))
            try:
                for a in p.find_all('a'):
                    pic_url = 'http://www.cidp.edu.cn' + a['href']
                    page_list.append({'pic': pic_url})
                    continue
            except:
                continue

            # 段落文字
            page_content = str.join(p.stripped_strings)
            page_list.append({'content': page_content})

        return page_list[:-4], public_time

    # def save_data(news_list):
    #     db = pymysql.connect("localhost:3306", "root", "pengyu1998", "wechatdb")
    #     cursor = db.cursor()
    #     for news in news_list:
    #         cursor.execute("INSERT INTO NEWS_NEWS")

