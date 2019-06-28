# -*- coding: utf-8 -*-

from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    path('news/', views.content, name='content'),
    path('list/', views.news_list, name='news_list')
]
