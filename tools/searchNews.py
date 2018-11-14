import requests
import re
from bs4 import BeautifulSoup


class GetNews:
    data = {
        'col': '1',
        'appid': '1',
        'webid': '1',
        'path': '/',
        'columnid': '',  # 321 为通知，52 为新闻，4662 为学术
        'sourceContentType': '1',
        'unitid': '17343',
        'webname': '防灾科技学院',
        'permissiontype': '0',
    }

    # 首页刷新和加载
    def change_page(self, num, page_type):

            url = 'http://fzxy.edu.cn/module/web/jpage/dataproxy.jsp?startrecord={start}&endrecord={end}&perpage=20' \
                .format(start=str(num), end=str(int(num) + 19))

            self.data['columnid'] = page_type
            r = requests.post(url, data=self.data)
            r.encoding = 'UTF-8'
            return r.text

    # 得到新闻列表
    def get_page_url(self, html):
        news_list = []
        for news in re.compile(r'.*?<tr(.*?)</tr>.*?').findall(html):
            # print(news)

            # 新闻标题，链接
            for result in re.compile(r'.*?href=\'(.*?).html\'.*?title=\'(.*?)\'').findall(news):
                title = result[1]
                url = 'http://www.fzxy.edu.cn{u}.html'.format(u=result[0])
                try:
                    # print('get:', title, url)
                    pub_time, content = self.get_info(url)
                except requests.exceptions:
                    continue

                news_list.append({'url': url, 'pub_time': pub_time, 'title': title, 'page_content': content})
        print('return')
        return news_list

    # 列表梗概
    @staticmethod
    def get_info(url):
        page = requests.get(url, timeout=5)
        page.encoding = 'utf-8-sig'
        html = page.text
        # print(html)
        # print(html[:10000])
        public_time = re.compile(r'.*?<meta name="PubDate" content="(.*?)\s\d+:\d+">').findall(html[:1500])
        # content = re.compile(r'.*?16px;">(.*?)</span><span.*?').findall(html)
        soup = BeautifulSoup(html[:10000], 'lxml')
        content = ''
        for p in soup.find_all('p')[:2]:
            item = ''
            page_content = item.join(p.stripped_strings)
            content += page_content
            # print(content)
        return public_time, content

    def get_page(self, url):
        page = requests.get(url)
        page.encoding = 'utf-8'
        html = page.text
        news_list = []
        for news in re.compile(r'.*?<tr(.*?)</tr>.*?').findall(html)[5:-1]:
            # print(news)

            # 新闻标题，链接
            for result in re.compile(r'.*?href=\'(.*?).html\'.*?title=\'(.*?)\'').findall(news):
                title = result[1]
                try:
                    purl = 'http://www.cidp.edu.cn' + result[0] + '.html'
                    print('get:', title, purl)
                    page_content, pub_time = self.get_news_content(purl)
                except BaseException:
                    continue

                news_list.append({'url': url, 'title': title, 'page_content': page_content, 'pub_time': pub_time})
        # print(news_list)
        return news_list


    def get_news_content(url):
        page = requests.get(url)
        page.encoding = 'utf-8'
        html = page.text
        pub_time = re.compile(r'<meta name="PubDate" content="(.*?)">').findall(html)[0]
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

        return page_list[:-4], pub_time

    # 直接获取单页内容
    def get_page_content(self, url):
        r = requests.get(url)
        # 服务器编码问题
        r.encoding = 'utf-8-sig'
        html = r.text
        # print(html)
        news_list = []
        title = re.compile(r'<meta name="ArticleTitle" content="(.*?)">').findall(html)[0]
        pub_time = re.compile(r'<meta name="PubDate" content="(.*?)">').findall(html)[0]
        print('get:', title, url)
        soup = BeautifulSoup(html, 'lxml')
        page_list = []
        pic_list = []
        for p in soup.find_all('p'):
            # print(p)
            # 拿到 a 标签里的图片链接
            # print(str.join(p.stripped_strings))
            try:
                for a in p.find_all('a'):
                    # print(a)
                    pic_url = 'http://www.cidp.edu.cn' + a['href']
                    page_list.append({'pic': pic_url})
                    pic_list.append(pic_url)
                    continue
                # for img in p.find_all('img'):
                #     # print(img)
                #     pic = 'http://www.cidp.edu.cn' + img['src']
                #     page_list.append({'pic': pic})
                #     pic_list.append(pic)
                #     continue
            except Exception as e:
                print(e)
                continue

            # 段落文字
            page_content = ' '.join(p.stripped_strings)
            page_list.append({'content': page_content})
        page_content = page_list[:-5]
        news_list.append({'title': title, 'pub_time': pub_time, 'url': url,
                          'page_content': page_content, 'pic_list': pic_list[:-2]})
        # print(news_list)
        return news_list

    def get_new_list(self, page, news_type):
        pass





    # def save_data(news_list):
    #     db = pymysql.connect("localhost:3306", "root", "pengyu1998", "wechatdb")
    #     cursor = db.cursor()
    #     for news in news_list:
    #         cursor.execute("INSERT INTO NEWS_NEWS")

