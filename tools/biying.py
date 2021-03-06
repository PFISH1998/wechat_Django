import requests
import json
import time


def request_api():
    api_url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    r = requests.get(api_url)
    image = json.loads(r.text)
    daily = structure_data(image)
    return daily


def structure_data(image):
    daily = dict()
    d = time.strftime("%b %d %Y", time.localtime()).split(' ')
    daily['pic_url'] = 'https://cn.bing.com' + image['images'][0]['url']
    daily['content'] = image['images'][0]['copyright']
    daily['mon'] = d[0]
    daily['day'] = int(str(d[1]))
    daily['year'] = d[2]
    return daily

# class Biying:
#     def __init__(self):
#         self.base_url = "https://cn.bing.com"
#         self.api = "/HPImageArchive.aspx?format=js&idx=0&n=1"
#
#
#     def