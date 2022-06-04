from django.urls import path

from .views import loginfunc, logoutfunc, signupfunc


app_name = 'welcome'
urlpatterns = [
    path('', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout', logoutfunc, name='logout'),
]
