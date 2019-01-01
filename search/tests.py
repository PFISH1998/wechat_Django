from django.test import TestCase
import requests
import json
# Create your tests here.

r = requests.get('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1')
image = json.loads(r.text)
print(image)
print(image['images'][0])
print(image['images'][0]['copyright'])
print(image['images'][0]['url'])
print(image['images'][0]['enddate'])