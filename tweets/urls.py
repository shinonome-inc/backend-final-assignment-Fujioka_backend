from django.urls import path

from tweets.views import TweetCreate, TweetDelete, delete_confirmfunc, detailfunc, listfunc


app_name = 'tweets'
urlpatterns = [
    path('', listfunc, name='list'),
    path('create/', TweetCreate.as_view(), name='create'),
    path('detail/<int:pk>', detailfunc, name='detail'),
    path('delete_confirm/<int:pk>', delete_confirmfunc, name='delete_confirm'),
    path('delete/<int:pk>', TweetDelete.as_view(), name='delete')
]
