from pydoc import cli
from django.shortcuts import render

# Create your views here.

import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import TweetModel


# Create your views here.

@login_required
def listfunc(request):
    tweet_list = TweetModel.objects.order_by('created_date').reverse().all()
    return render(request, 'tweets/list.html', {'tweet_list': tweet_list})

# @login_required
# def createfunc(request):
#     form = TweetModel(request.POST or None)
#     context = {'form': form}
#     if request.method == 'POST':
#         form = TweetModel(request.POST)
#         if form.is_valid():
#             form.clean_data.save()
#             return render(request, 'list.html', {})
#         # form.save()
#         # return render(request, 'list.html', {})

#     return render(request, 'tweets/create.html', context)

class TweetCreate(CreateView):
    model = TweetModel
    template_name = 'tweets/create.html'
    fields = ('text', 'author')
    success_url = reverse_lazy('tweets:list')
    
    
@login_required
def detailfunc(request, pk):
    tweet = get_object_or_404(TweetModel, pk=pk)
    return render(request, 'tweets/detail.html', {'tweet': tweet})


@login_required
def goodfunc(request, pk):
    tweet = get_object_or_404(TweetModel, pk=pk)
    clicked_user_name = request.user.get_username()
    if clicked_user_name in tweet.good_user_list:
        tweet.good -= 1
        tweet.good_user_list = tweet.good_user_list.replace('|'+clicked_user_name, '')
        tweet.save()
        return redirect('tweets:list')
    else :
        tweet.good += 1
        tweet.good_user_list = tweet.good_user_list + '|' + clicked_user_name
        tweet.save()
        return redirect('tweets:list')
    
    
@login_required
def badfunc(request, pk):
    tweet = get_object_or_404(TweetModel, pk=pk)
    clicked_user_name = request.user.get_username()
    if clicked_user_name in tweet.bad_user_list:
        tweet.bad -= 1
        tweet.bad_user_list = tweet.bad_user_list.replace('|'+clicked_user_name, '')
        tweet.save()
        return redirect('tweets:list')
    else :
        tweet.bad += 1
        tweet.bad_user_list = tweet.bad_user_list + '|' + clicked_user_name
        tweet.save()
        return redirect('tweets:list')
    
    
