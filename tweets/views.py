from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView


from tweets.models import TweetModel


@login_required
def testfunc(request):
    return render(request, 'tweets/test.html')


@login_required
def listfunc(request):
    tweet_list = TweetModel.objects.order_by('created_date').reverse().all()
    return render(request, 'tweets/list.html', {'tweet_list': tweet_list})

class TweetCreate(CreateView):
    model = TweetModel
    template_name = 'tweets/create.html'
    fields = ('text', 'author')
    success_url = reverse_lazy('tweets:list')
    
@login_required
def detailfunc(request, pk):
    tweet = get_object_or_404(TweetModel, pk=pk)
    return render(request, 'tweets/detail.html', {'tweet': tweet})
