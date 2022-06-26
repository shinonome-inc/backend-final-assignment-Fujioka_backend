from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import CreateForm


def signupfunc(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('tweets:test')
    else:
        form = CreateForm()
    return render(request, 'accounts/signup.html', {'form': form})
