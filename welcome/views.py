import re
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.


def welcome_func(request):
    return render(request, 'welcome/welcome.html')


def login_func(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tweets:list')
        else:
            return render(request, 'welcome/login.html', {'error': 'This user is not exitst. Please try anothor name or passwrod.'})

    return render(request, 'welcome/login.html', {})


@login_required
def logout_func(request):
    logout(request)
    return redirect('welcome:login')
