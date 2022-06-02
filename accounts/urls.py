from django.urls import path, include
from django.views.generic import TemplateView


from .views import followingfunc, profilefunc, goodfunc, badfunc, destoryer, followerfunc, followeefunc

app_name = 'accounts'
urlpatterns = [
    path('profile/<str:username>', profilefunc, name='profile'),
    path('good/<int:pk>/<str:author>', goodfunc, name='good'),
    path('bad/<int:pk>/<str:author>', badfunc, name='bad'),
    path('following/<str:followeename>', followingfunc, name='following'),
    path('follower/<str:username>', followerfunc, name='follower'),
    path('followee/<str:username>', followeefunc, name='followee'),
    
    
    #以下は触らない
    path('destory/', destoryer, name='destory'),
    path('test/', TemplateView.as_view(template_name='accounts/profile.html'), name='test'),
    
    
    # path('', views.WelcomeView.as_view(), name='welcome'),
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('home/', views.HomeView.as_view(), name='home'),
    # path('', include('django.contrib.auth.urls')),
    # path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    # path('profile/edit/', views.UserProfileEditView.as_view(), name='user_profile_edit'),
    # path('<str:username>/following_list/', views.FollowingListView.as_view(), name='following_list'),
    # path('<str:username>/follower_list/', views.FollowerListView.as_view(), name='follower_list'),
    # path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    # path('<str:username>/unfollow/', views.UnFollowView, name='unfollow'),
]
