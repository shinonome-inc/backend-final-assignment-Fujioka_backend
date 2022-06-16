from django.urls import path
from django.views.generic import TemplateView

from tweets.views import testfunc


app_name = 'tweets'
urlpatterns = [
    path('test/', testfunc, name='test'),
]
