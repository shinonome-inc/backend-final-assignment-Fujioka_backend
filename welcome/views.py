from django.shortcuts import render

# Create your views here.


from django.db import IntegrityError
from django.shortcuts import render
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from accounts.models import User

# Create your views here.

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '', password)
            login(request, user)
            # return redirect('tweets:list')
            return redirect('tweets:test')
        except IntegrityError:
            return render(request, 'welcome/signup.html', {'error': 'Sorry, This name has been already used.'})
        
    return render(request, 'welcome/signup.html')


def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect('tweets:list')
            return redirect('tweets:test')
        else:
            return render(request, 'welcome/login.html', {'error':'This user is not exitst. Please try anothor name or passwrod.'})
        
    return render(request, 'welcome/login.html', {})


@login_required
def logoutfunc(request):
    logout(request)
    return redirect('welcome:login')

