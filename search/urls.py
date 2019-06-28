# -*- coding: utf-8 -*-

from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home),
    path('grade', views.grade, name='grade'),
    path('table', views.time_table, name='time_table'),
    path('register', views.register)
]
