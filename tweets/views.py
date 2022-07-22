import json
from typing import Any, TypedDict
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.views.generic.edit import BaseCreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


from tweets.models import TweetModel, LikeModel


@login_required
def test_func(request):
    return render(request, 'tweets/test.html')


@login_required
def list_func(request):
    tweet_list = TweetModel.objects.order_by('created_date').reverse().all()
    
    # tweet_listのなかに、ユーザーが既にいいねを押したツイートを選別する
    # liked_tweets = map(lambda tweet: tweet.pk if tweet.likemodel_set.filter(user = request.user) else None, tweet_list)
    liked_tweets = request.user.likemodel_set.values_list('tweet', flat=True)
            
    context = {
        'tweet_list': tweet_list,
        'liked_tweets': liked_tweets,
    }
    return render(request, 'tweets/list.html', context)

class TweetCreate(LoginRequiredMixin, CreateView):
    model = TweetModel
    template_name = 'tweets/create.html'
    fields = ('text',)
    success_url = reverse_lazy('tweets:list')
    
    def post(self, request, *args, **kwargs):
        self.object = TweetModel(author = self.request.user)
        return super(BaseCreateView, self).post(request, *args, **kwargs)
    
    
@login_required
def detail_func(request, pk):
    client_user = request.user
    tweet = get_object_or_404(TweetModel, pk=pk)
    author = tweet.author
    identity = True if client_user == author else False
    liked_tweets = request.user.likemodel_set.values_list('tweet', flat=True)
    
    context = {
        'tweet': tweet,
        'identity': identity,
        'liked_tweets': liked_tweets,
    }
    return render(request, 'tweets/detail.html', context)


@login_required
def delete_confirm_func(request, pk):
    client_user = request.user
    author = get_object_or_404(TweetModel, pk=pk).author
    if client_user == author:
        return redirect('tweets:delete', pk = pk)
    else :
        return redirect('tweets:list')


class TweetDelete(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
    model = TweetModel
    template_name = 'tweets/delete.html'
    success_url = reverse_lazy('tweets:list')
    
    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user


@login_required
def like_func(request):
    # Django Database 関連の処理
    # POST送信かを確認
    if request.method == 'POST' :
        # jsonファイルを取得
        json_body = request.body.decode("utf-8")
        body = json.loads(json_body)
        # POST送信の中にtweet_pkが入っているかを確認
        if body['tweet_pk']:
            tweet = get_object_or_404(TweetModel, pk=body['tweet_pk'])
            user = request.user
            is_liked = False
            like = LikeModel.objects.filter(tweet = tweet, user = user)
            
            dataType = TypedDict('dataType', {'tweet': TweetModel, 'user': Any, 'is_liked': bool, 'like': Any})
            data: dataType = dict(tweet=tweet, user=user, is_liked=is_liked, like=like)
            
            # tweetがすでにいいねされていたら解除、そうでなければいいね作成
            # 変数の変更はいいねが押されているかの判別のis_likedに限定すること
            # それ以外の処理はLikeHnadleに記載する
            if like.exists():
                # いいね解除の処理
                is_liked = LikeHandle.deletelike_func(data)
            else:
                # いいね作成の処理
                is_liked = LikeHandle.createlike_func(data)
                
            context = {
                'tweet_pk': tweet.pk,
                'is_liked': is_liked,
                'count': tweet.likemodel_set.count(),
            }
            # Json形式でcontextを送信。javascriptでスタイルの処理を行う
            return JsonResponse(context)
        
        else:
            # postの内容物のエラーハンドリング
            return JsonResponse({})

class LikeHandle():
    dataType = TypedDict('dataType', {'tweet': TweetModel, 'user': Any, 'is_liked': bool, 'like': Any})
    
    # いいね解除の処理
    def deletelike_func(data: dataType):
        data['like'].delete()
        return data['is_liked']
    
    # いいね作成の処理
    def createlike_func(data: dataType):
        data['like'].create(tweet = data['tweet'], user = data['user'])
        data['is_liked'] = True
        return data['is_liked']
