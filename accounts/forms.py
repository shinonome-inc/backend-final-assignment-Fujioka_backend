# from django import forms

from .models import User
from django.contrib.auth.forms import UserCreationForm



class CreateForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        