from django.urls import path

from .views import display_follower_func, display_following_func, profile_func, signup_func, follow_func


app_name = 'accounts'
urlpatterns = [
    path('signup/', signup_func, name='signup'),
    path('profile/<int:user_pk>', profile_func, name='profile'),
    path('follow/', follow_func, name='follow'),
    path('following/<int:user_pk>', display_following_func, name='display_following'),
    path('follower/<int:user_pk>', display_follower_func, name='display_follower'),
]
