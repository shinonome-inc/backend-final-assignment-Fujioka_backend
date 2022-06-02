from pprint import pprint
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from .models import User
from tweets.models import TweetModel

# Create your views here.

@login_required
def profilefunc(request, username):
    clicked_user_name = request.user.get_username()
    account = get_object_or_404(User, username=username)
    follow_detecting = True if clicked_user_name in account.follower  else False
    own_profile_detecting = True if clicked_user_name == username else False
    try :
        user_tweets = get_list_or_404(TweetModel, author=username)
        tweets_exist = True
    except :
        user_tweets = ''
        tweets_exist = False
    context = {
        'account': account,
        'user_tweets': user_tweets,
        'tweets_exist': tweets_exist,
        'follow_detecting': follow_detecting,
        'own_profile_detecting': own_profile_detecting,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def goodfunc(request, pk, author):
    tweet = get_object_or_404(TweetModel, pk=pk)
    clicked_user_name = request.user.get_username()
    if clicked_user_name in tweet.good_user_list:
        tweet.good -= 1
        tweet.good_user_list = tweet.good_user_list.replace('|'+clicked_user_name, '')
        tweet.save()
        return redirect('accounts:profile', username=author)
    else :
        tweet.good += 1
        tweet.good_user_list = tweet.good_user_list + '|' + clicked_user_name
        tweet.save()
        return redirect('accounts:profile', username=author)
    
    
@login_required
def badfunc(request, pk, author):
    tweet = get_object_or_404(TweetModel, pk=pk)
    clicked_user_name = request.user.get_username()
    if clicked_user_name in tweet.bad_user_list:
        tweet.bad -= 1
        tweet.bad_user_list = tweet.bad_user_list.replace('|'+clicked_user_name, '')
        tweet.save()
        return redirect('accounts:profile', username=author)
    else :
        tweet.bad += 1
        tweet.bad_user_list = tweet.bad_user_list + '|' + clicked_user_name
        tweet.save()
        return redirect('accounts:profile',  username=author)
    

# def testfollowingfunc(request, followeename):
#     followee_user = get_object_or_404(User, username=followeename)
#     followee_user.follower_number += 1
#     followee_user.save()
#     return redirect('accounts:profile', username=followeename)
    
    
@login_required
def followingfunc(request, followeename):
    clicked_user_name = request.user.get_username()
    followee_user = get_object_or_404(User, username=followeename)
    following_user = get_object_or_404(User, username=clicked_user_name)
    check = True if clicked_user_name in followee_user.follower else False
    
    followee_handlingfunc(followee_user, clicked_user_name, check)
    following_handlingfunc(following_user, followeename, check)
    
    return redirect('accounts:profile', username=followeename)
    
    


def followee_handlingfunc(followee_user, clicked_user_name, check):
    if check:
        followee_user.follower_number -= 1
        followee_user.follower = followee_user.follower.replace('|'+clicked_user_name, '')
        followee_user.save()
    else :
        followee_user.follower_number += 1
        followee_user.follower = followee_user.follower + '|' + clicked_user_name
        followee_user.save()
    
def following_handlingfunc(following_user, followeename, check):
    if check:
        following_user.following_number -= 1
        following_user.following = following_user.following.replace('|'+followeename, '')
        following_user.save()
    else :
        following_user.following_number += 1
        following_user.following = following_user.following + '|' + followeename
        following_user.save()
    
    
def followerfunc(request, username):
    user = get_object_or_404(User, username=username)
    follower = user.follower[1:]
    follower_list = follower.split('|')
    context = {
        'username':user.username,
        'follower_list':follower_list,
    }
    return render(request, 'accounts/follower.html', context)
    
    
def followeefunc(request, username):
    user = get_object_or_404(User, username=username)
    followee = user.following[1:]
    followee_list = followee.split('|')
    context = {
        'username':user.username,
        'follower_list':followee_list,
    }
    return render(request, 'accounts/follower.html', context)
    
    
    
    
    
    
#以下は触らない


def destoryer(request):
    users = get_list_or_404(User)
    for user in users:
        user.follower = ''
        user.follower_number = 0
        user.following = ''
        user.following_number = 0
        user.save()
    return redirect('tweets:list')
        