from bs4 import BeautifulSoup
import requests
import re

# page_url = "http://www.cidp.edu.cn/index/xwzx.htm"


def get_url_from_index_page(page_type):
    page_url = "http://www.cidp.edu.cn/index/" + page_type + '.htm'
    print(page_url)
    r = requests.get(page_url)
    r.encoding = 'utf-8'
    page = re.compile(r'.*?<div class="list_main_right">(.*?)</div>.*?', re.S).findall(r.text)  # 主内容区域
    next_page = re.compile(r'<span class="p_next p_fun"><a href="(.*?)">下页</a></span>.*?').findall(r.text)[0]  # 获取下页页码
    news_list = []
    soup = BeautifulSoup(str(page), 'lxml')
    for i in soup.find_all('a'):
        news_url = re.findall(r'.*?href="(.*?)"', str(i))[0]
        print(news_url)
        single = get_index_content_from_url(news_url)
        news_list.append(single)

    page = dict()
    page.update({'news_list': news_list, 'next_page': next_page[:-4]})
    print(page)
    return page


def get_index_content_from_url(news_url):  # 获取内容
    print(news_url)

    if news_url.startswith('tp://211.71.233.21'):  # 旧版网页
        return {""}

    # news_url = news_url
    content_url = 'http://www.cidp.edu.cn' + news_url
    print(content_url)
    r = requests.get(str(content_url))
    r.encoding = 'utf-8'
    page = r.text
    title = re.findall(r'.*?<h1 class="c-title">(.*?)</h1>', page)[0]
    description = re.findall(r'<META Name="description" Content="(.*?)"', page)[0]
    pub_time = re.findall(r'<div class="other-s">发布日期：(.*?)&nbsp;&nbsp;', page)[0]
    page_info = dict()
    page_info.update({'title': title, 'pub_time': pub_time, 'description': description, 'url': news_url})
    # print(page_info)
    return page_info

def get_total_content(news_url='http://www.cidp.edu.cn/info/1043/6604.htm'):
    r = requests.get(news_url)
    r.encoding = 'utf-8'
    html = r.text
    print(r.text)
    tap = re.findall('')
    soup = BeautifulSoup(html, 'lxml')
    page_list = []
    for content in soup.find_all('p'):
        for img in content.find_all('img'):
            pic_url = 'http://www.cidp.edu.cn' + img['src']
            page_list.append({'pic': pic_url})
            continue
        text = ' '.join([i for i in content.strings])
        page_list.append({'content': text})
        # print(content.string)
    print(page_list[:-5])