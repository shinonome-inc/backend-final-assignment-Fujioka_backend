from django.urls import path

from .views import loginfunc, logoutfunc, welcomefunc


app_name = 'welcome'
urlpatterns = [
    path('', welcomefunc, name='welcome'),
    path('login/', loginfunc, name='login'),
    path('logout', logoutfunc, name='logout'),
]
