from tkinter import CASCADE
from django.db import models
from django.utils import timezone

from accounts.models import User


class TweetModel(models.Model):
    text = models.TextField(max_length=140)
    good = models.IntegerField(null=True, blank=True, default=0)
    bad = models.IntegerField(null=True, blank=True, default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    good_user_list = models.TextField(null=True, blank=True, default='')
    bad_user_list = models.TextField(null=True, blank=True, default='')
    
    def __str__(self):
        return self.text[:7]
