from . import views
from django.urls import path

app_name = 'circle'
urlpatterns = [
    path('post/', views.PostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),

    path('user/', views.CircleUserList.as_view()),
    path('user/<int:pk>/', views.CircleUserDetail.as_view()),

    path('comments/<int:pk>/', views.CommentsList.as_view()),

    path('like/<int:pk>/', views.LikeList.as_view())

]
