from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.views.generic.edit import BaseCreateView


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
    fields = ('text',)
    success_url = reverse_lazy('tweets:list')
    
    def post(self, request, *args, **kwargs):
        self.object = TweetModel(author = self.request.user)
        return super(BaseCreateView, self).post(request, *args, **kwargs)
    
    
@login_required
def detailfunc(request, pk):
    client_user = request.user.get_username()
    author = request.GET['author']
    identity = True if client_user == author else False
    tweet = get_object_or_404(TweetModel, pk=pk)
    context = {
        'tweet': tweet,
        'identity': identity,
    }
    return render(request, 'tweets/detail.html', context)

@login_required
def delete_confirmfunc(request, pk):
    client_user = request.user.get_username()
    author = request.GET['author']
    if client_user == author:
        return redirect('tweets:delete', pk = pk)
    else :
        return redirect('tweets:list')

class TweetDelete(DeleteView):
    model = TweetModel
    template_name = 'tweets/delete.html'
    success_url = reverse_lazy('tweets:list')
