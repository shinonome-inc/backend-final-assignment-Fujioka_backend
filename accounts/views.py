from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from accounts.models import User
from tweets.models import TweetModel

from .forms import CreateForm


def signupfunc(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('tweets:list')
    else:
        form = CreateForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profilefunc(request, user_pk):
    # 使用しているユーザと、クリックされたユーザを取得
    client_user = request.user
    account = get_object_or_404(User, pk=user_pk)
    # これらのユーザが同一人物家を確認
    identity = True if client_user == account else False
    
    # フォローしているかの確認
    follow_detecting = False
    if (identity == False) :
        follow_detecting = True if account in client_user.following_user.values_list('following_user', flat=True) else False
    

    # ツイートの取得
    try:
        user_tweets = get_list_or_404(TweetModel.objects.order_by(
            'created_date').reverse().all(), author=account)
    except:
        user_tweets = False
    tweets_exist = True if user_tweets else False

    context = {
        'account': account,
        'user_tweets': user_tweets,
        'tweets_exist': tweets_exist,
        'identify': identity,
        'follow_detecting': follow_detecting,
    }

    return render(request, 'accounts/profile.html', context)
