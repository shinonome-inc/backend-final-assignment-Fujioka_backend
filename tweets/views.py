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
def testfunc(request):
    return render(request, 'tweets/test.html')


@login_required
def listfunc(request):
    tweet_list = TweetModel.objects.order_by('created_date').reverse().all()
    liked_tweets = []
    for tweet in tweet_list:
        liked = tweet.likemodel_set.filter(user = request.user)
        if liked.exists():
            liked_tweets.append(tweet.pk)
            
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
def detailfunc(request, pk):
    client_user = request.user
    tweet = get_object_or_404(TweetModel, pk=pk)
    author = tweet.author
    identity = True if client_user == author else False
    context = {
        'tweet': tweet,
        'identity': identity,
    }
    return render(request, 'tweets/detail.html', context)


@login_required
def delete_confirmfunc(request, pk):
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
def likefunc(request):
    if request.method == 'POST' and request.POST.get('csrfmiddlewaretoken'):
        tweet = get_object_or_404(TweetModel, pk=request.POST.get('tweet_pk'))
        user = request.user
        liked = False
        like = LikeModel.objects.filter(tweet = tweet, user = user)
        if like.exists():
            like.delete()
        else:
            like.create(tweet = tweet, user = user)
            liked = True
            
        context = {
            'tweet_pk': tweet.pk,
            'liked': liked,
            'count': tweet.likemodel_set.count(),
        }
        return JsonResponse(context)
    
    else: 
        pass
