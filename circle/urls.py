from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path

app_name = 'circle'
urlpatterns = [
    path('post/', views.PostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),

    path('user/', views.CircleUserList.as_view()),
    path('user/<int:pk>/', views.CircleUserDetail.as_view()),

    path('comments/<int:pk>/', views.CommentsList.as_view()),
    path('comments-note/<int:pk>/', views.CommentNoteList.as_view()),

    path('like/<int:pk>/', views.LikeList.as_view()),

    path('uid/', views.get_open_id)

]

# urlpatterns = format_suffix_patterns(urlpatterns)
