import requests
import re
from bs4 import BeautifulSoup


class One:
    def __init__(self):
        self.url = 'http://wufazhuce.com'

    def get_page(self):
        r = requests.get(self.url)
        daily = dict()
        soup = BeautifulSoup(r.text, 'lxml')
        content = soup.find('div', class_='item active')
        content = str(content)
        daily['pic_url'] = re.findall(r'.*?src="(.*?)"/>.*?>', content)[0]
        daily['content'] = re.findall(r'.*?<a href="http://wufazhuce.com/one/\d+">(.*?)</a> </div>.*?', content)[0]
        daily['num'] = re.findall(r'.*?<p class="titulo">(.*?)</p>.*?', content)[0]
        daily['mon'] = re.findall(r'.*?<p class="may">(.*?)</p>.*?', content)[0]
        daily['day'] = re.findall(r'.*?<p class="dom">(.*?)</p>.*?', content)[0]
        return daily
