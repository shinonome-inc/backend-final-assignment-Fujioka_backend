from django.urls import path, include
from django.views.generic import TemplateView


from .views import signupfunc

app_name = 'accounts'
urlpatterns = [

    path('signup/', signupfunc, name='signup'),
    

]
