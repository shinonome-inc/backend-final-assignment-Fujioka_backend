from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def testfunc(request):
    return render(request, 'tweets/test.html')

def commit_test_func(request):
    pass
