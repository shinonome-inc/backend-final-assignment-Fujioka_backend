import json
from typing import TypedDict
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from accounts.models import FollowModel, User
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
    clicked_account = get_object_or_404(User, pk=user_pk)
    # これらのユーザが同一人物家を確認
    is_same_user: bool = True if client_user == clicked_account else False
    
    # フォローしているかの確認
    follow_detecting = False
    if (is_same_user == False) :
        follow_detecting = True if clicked_account.pk in client_user.following_user.values_list('follower_user', flat=True) else False
    

    # ツイートの取得
    user_tweets = TweetModel.objects.filter(author=clicked_account).order_by('created_date').reverse().all()
    tweets_exist = True if user_tweets else False

    # いいねしているツイートの取得
    liked_tweets = request.user.likemodel_set.values_list('tweet', flat=True)

    context = {
        'clicked_account': clicked_account,
        'user_tweets': user_tweets,
        'tweets_exist': tweets_exist,
        'is_same_user': is_same_user,
        'follow_detecting': follow_detecting,
        'liked_tweets': liked_tweets,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def followfunc(request):
    # JSからのPOST受け取り
    if request.method == 'POST':
        json_body = request.body.decode("utf-8")
        body = json.loads(json_body)
        # postの中に適切なデータが入っているか確認
        if body['client_pk'] and body['account_pk'] and body['client_pk'] != body['account_pk']:
            client = get_object_or_404(User, pk=body['client_pk'])
            clicked_account = get_object_or_404(User, pk=body['account_pk'])
            
            # フォローしているかの再確認
            is_followed = True if clicked_account.pk in client.following_user.values_list('follower_user', flat=True) else False

            dataType = TypedDict('dataType', {'client': User, 'clicked_account': User})
            data: dataType = dict(client = client, clicked_account = clicked_account)
            # フォローしていたときの処理
            if is_followed:
                FollowHandle.delete_followfunc(data)
            # フォローしていなかったときの処理
            else:
                FollowHandle.create_followfunc(data)

            context = {
                'is_followed': not is_followed,
                'follower_number': clicked_account.follower_user.count(),
            }
            return JsonResponse(context)
        
        else:
            # postの内容物が揃っていなかったときのエラーハンドリング
            return JsonResponse({})
    

class FollowHandle():
    dataType = TypedDict('dataType', {'client': User, 'clicked_account': User})
    
    # フォローしていたときの処理
    def delete_followfunc(data: dataType):
        follow = get_object_or_404(FollowModel, following_user=data['client'], follower_user=data['clicked_account'])
        follow.delete()

    # フォローしていなかったときの処理
    def create_followfunc(data: dataType):
        FollowModel.objects.create(following_user=data['client'], follower_user=data['clicked_account'])
