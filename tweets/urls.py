from django.urls import path

from tweets.views import TweetCreate, TweetDelete, delete_confirm_func, detail_func, like_func, list_func


app_name = 'tweets'
urlpatterns = [
    path('', list_func, name='list'),
    path('create/', TweetCreate.as_view(), name='create'),
    path('detail/<int:pk>', detail_func, name='detail'),
    path('delete_confirm/<int:pk>', delete_confirm_func, name='delete_confirm'),
    path('delete/<int:pk>', TweetDelete.as_view(), name='delete'),
    path('like', like_func, name='like')
]
