from . import views
from django.urls import path

app_name = 'news'
urlpatterns = [
    path('news/', views.content, name='content'),
    path('list/', views.news_list, name='news_list')
]
