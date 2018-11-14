from . import views
from django.urls import path

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('grade', views.grade, name='grade'),
    path('table', views.time_table, name='time_table'),
    path('register', views.register)
]
