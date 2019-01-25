from bs4 import BeautifulSoup
import requests
import re

# page_url = "http://www.cidp.edu.cn/index/xwzx.htm"


def get_url_from_index_page(url):
    page_url = 'http://www.cidp.edu.cn/index/{}.htm'.format(url)
    # print(page_url)
    r = requests.get(page_url)
    r.encoding = 'utf-8'
    page = re.compile(r'.*?<div class="list_main_right">(.*?)</div>.*?', re.S).findall(r.text)  # 主内容区域
    next_page = re.compile(r'<span class="p_next p_fun"><a href=".*?(\d+).htm">下页</a></span>.*?').findall(r.text)[0]  # 获取下页页码
    news_list = []
    soup = BeautifulSoup(str(page), 'lxml')
    for i in soup.find_all('a'):
        news_url = re.findall(r'.*?href="(.*?)"', str(i))[0]
        single = get_index_content_from_url(news_url)
        news_list.append(single)

    page = dict()
    page.update({'news_list': news_list, 'next_page': next_page})
    # print(page)
    return page


def get_index_content_from_url(news_url):  # 获取内容
    if news_url.startswith('http://211.71.233.21'):  # 旧版网页
        # print("old")
        return
    real_url = re.findall(r'.*?/(\d+)/(\d+).htm', news_url)[0]
    content_url = 'http://www.cidp.edu.cn/info/{}/{}.htm'\
        .format(real_url[0], real_url[1])
    try:
        r = requests.get(str(content_url))
        r.encoding = 'utf-8'
        status = r.status_code
        if status == 200:
            page = r.text
            title = re.findall(r'.*?<h1 class="c-title">(.*?)</h1>', page)[0]
            description = re.findall(r'<META Name="description" Content="(.*?)"', page)[0]
            pub_time = re.findall(r'<div class="other-s">发布日期：(.*?)&nbsp;&nbsp;', page)[0]
            page_info = dict()
            page_info.update({'title': title, 'pub_time': pub_time, 'description': description, 'url': news_url})
            # print(page_info)
            return page_info
        elif status == 404:
            pass

            # raise Exception('url')
    except Exception as e:
        print(e)


def get_total_content(url):
    page = re.findall(r'.*?/(\d+)/(\d+).htm', url)[0]
    news_url = 'http://www.cidp.edu.cn/info/{}/{}.htm'.format(page[0], page[1])
    r = requests.get(news_url)
    r.encoding = 'utf-8'
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    page_list = []
    img_list = []
    for content in soup.find_all('p'):
        for img in content.find_all('img'):
            pic_url = 'http://www.cidp.edu.cn' + img['src']
            img_list.append(pic_url)
            page_list.append({'pic': pic_url})
            continue
        text = ' '.join([i for i in content.strings])
        page_list.append({'content': text})
        # print(content.string)
    # print(page_list)
    return page_list[:-4], img_list