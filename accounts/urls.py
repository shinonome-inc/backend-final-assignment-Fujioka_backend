from django.urls import path

from .views import profilefunc, signupfunc


app_name = 'accounts'
urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('profile/<int:user_pk>', profilefunc, name='profile'),
]
