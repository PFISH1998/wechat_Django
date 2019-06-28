from django.test import TestCase
from tools.searchNews import GetNews
from tools.IdriverManage import Search
# from news.models import News
from search import models

# Create your tests here.

g = GetNews()
html = g.get_page('http://211.71.233.21/col/col321/index.html?uid=17343&pageNum=1')
g.get_page(html)
