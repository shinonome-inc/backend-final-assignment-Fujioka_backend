from django.urls import path
from django.contrib.auth import views as auth_views

from .views import login_func, logout_func, welcome_func


app_name = 'welcome'
urlpatterns = [
    path('', welcome_func, name='welcome'),
    path('login/', login_func, name='login'),
    path('logout', logout_func, name='logout'),
]
