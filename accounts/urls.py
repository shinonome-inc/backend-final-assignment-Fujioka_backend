from django.urls import path

from .views import signupfunc


app_name = 'accounts'
urlpatterns = [
    path('signup/', signupfunc, name='signup'),
]
