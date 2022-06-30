from django.urls import path

from tweets.views import TweetCreate, detailfunc, listfunc


app_name = 'tweets'
urlpatterns = [
    path('', listfunc, name='list'),
    path('create/', TweetCreate.as_view(), name='create'),
    path('detail/<int:pk>', detailfunc, name='detail'),
]
