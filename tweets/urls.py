from django.urls import path
from django.views.generic import TemplateView





app_name = 'tweets'
urlpatterns = [

    
    #確認用テストページ
    path('test/', TemplateView.as_view(template_name='tweets/test.html'), name='test'),
    
   
]
