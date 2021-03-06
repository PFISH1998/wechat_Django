from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path

app_name = 'circle'
urlpatterns = [
    path('posts', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),

    path('user/', views.CircleUserList.as_view()),
    path('user/<int:pk>/', views.CircleUserDetail.as_view()),

    path('comments/<int:pk>/', views.CommentsList.as_view()),
    path('comments-note/<int:pk>/', views.CommentNoteList.as_view()),

    path('like/<int:pk>/', views.LikeList.as_view()),

    path('uid/', views.get_open_id),

    path('pic/', views.file_upload)

]

# urlpatterns = format_suffix_patterns(urlpatterns)
