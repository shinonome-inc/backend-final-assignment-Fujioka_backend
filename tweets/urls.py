from django.urls import path
from django.views.generic import TemplateView

from .views import TweetCreate, badfunc, detailfunc, goodfunc, listfunc




app_name = 'tweets'
urlpatterns = [
    path('', listfunc, name='list'),
    # path('create/', createfunc, name='create'),
    path('create/', TweetCreate.as_view(), name='create'),
    path('detail/<int:pk>', detailfunc, name='detail'),
    path('good/<int:pk>', goodfunc, name='good'),
    path('bad/<int:pk>', badfunc, name='bad'),
    
    #確認用テストページ
    path('test/', TemplateView.as_view(template_name='tweets/test.html'), name='test'),
    
    
    # path('', TemplateView.as_view(template_name='tweets/test.html'), name='test'),
    # path('create/', views.TweetCreateView.as_view(), name='create'),
    # path('<int:pk>/', views.TweetDetailView.as_view(), name='detail'),
    # path('<int:pk>/delete/', views.TweetDeleteView.as_view(), name='delete'),
    # path('<int:pk>/like/', views.LikeView, name='like'),
    # path('<int:pk>/unlike/', views.UnlikeView, name='unlike'),
]
