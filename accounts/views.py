import json
from typing import TypedDict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from accounts.models import FollowModel, User
from tweets.models import TweetModel

from .forms import CreateForm


def signup_func(request):
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
def profile_func(request, user_pk):
    # 使用しているユーザと、クリックされたユーザを取得
    request_user = request.user
    profile_user = get_object_or_404(User, pk=user_pk)
    # これらのユーザが同一人物家を確認
    is_same_user: bool = request_user == profile_user
    
    # フォローしているかの確認
    is_followed = FollowModel.objects.filter(following_user=request_user, follower_user=profile_user).exists()

    # ツイートの取得
    user_tweets = TweetModel.objects.filter(author=profile_user).order_by('created_date').reverse().all()
    tweets_exist = user_tweets.exists()

    # いいねしているツイートの取得
    liked_tweets = request.user.likemodel_set.values_list('tweet', flat=True)

    context = {
        'profile_user': profile_user,
        'user_tweets': user_tweets,
        'tweets_exist': tweets_exist,
        'is_same_user': is_same_user,
        'is_followed': is_followed,
        'liked_tweets': liked_tweets,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def follow_func(request):
    # JSからのPOST受け取り
    if request.method == 'POST':
        json_body = request.body.decode("utf-8")
        body = json.loads(json_body)
        # postの中に適切なデータが入っているか確認
        if body['account_pk'] :
            request_user = request.user
            profile_user = get_object_or_404(User, pk=body['account_pk'])
            # 自分自身へのフォローではないか
            if request_user != profile_user :
                # フォローしているかの再確認
                is_followed = profile_user.pk in request_user.following_user.values_list('follower_user', flat=True)

                dataType = TypedDict('dataType', {'request_user': User, 'profile_user': User})
                data: dataType = dict(request_user = request_user, profile_user = profile_user)
                # フォローしていたときの処理
                if is_followed:
                    FollowHandle.delete_follow_func(data)
                # フォローしていなかったときの処理
                else:
                    FollowHandle.create_follow_func(data)

                context = {
                    'is_followed': not is_followed,
                    'follower_number': profile_user.follower_user.count(),
                }
                return JsonResponse(context)
            
            else:
                # 自分自身へのフォローをしようとしたときのエラーハンドリング
                return JsonResponse({})
        else:
            # postの内容物が揃っていなかったときのエラーハンドリング
            return JsonResponse({})
    

class FollowHandle():
    dataType = TypedDict('dataType', {'request_user': User, 'profile_user': User})
    
    # フォローしていたときの処理
    def delete_follow_func(data: dataType):
        follow = get_object_or_404(FollowModel, following_user=data['request_user'], follower_user=data['profile_user'])
        follow.delete()

    # フォローしていなかったときの処理
    def create_follow_func(data: dataType):
        FollowModel.objects.create(following_user=data['request_user'], follower_user=data['profile_user'])


@login_required
def display_following_func(request, user_pk):
    profile_user = get_object_or_404(User, pk=user_pk)
    follow_model_including_following_user = FollowModel.objects.filter(following_user=profile_user)
    following_user_list = list(map(lambda follow_model: get_object_or_404(User, pk=follow_model.follower_user_id), follow_model_including_following_user))
    context = {
        'profile_user': profile_user,
        'following_user_list': following_user_list,
    }
    return render(request, 'accounts/following.html', context)

@login_required
def display_follower_func(request, user_pk):
    profile_user = get_object_or_404(User, pk=user_pk)
    follow_model_including_follower_user = FollowModel.objects.filter(follower_user=profile_user)
    follower_user_list = list(map(lambda follow_model: get_object_or_404(User, pk=follow_model.following_user_id), follow_model_including_follower_user))
    context = {
        'profile_user': profile_user,
        'follower_user_list': follower_user_list,
    }
    return render(request, 'accounts/follower.html', context)
