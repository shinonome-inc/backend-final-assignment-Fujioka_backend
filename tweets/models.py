
# class Tweet(models.Model):
#     pass

from django.db import models
from django.utils import timezone


class TweetModel(models.Model):
    text = models.TextField(max_length=140)
    good = models.IntegerField(null=True, blank=True, default=0)
    bad = models.IntegerField(null=True, blank=True, default=0)
    author = models.CharField(max_length=50)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    good_user_list = models.TextField(null=True, blank=True, default='')
    bad_user_list = models.TextField(null=True, blank=True, default='')
    
    def __str__(self):
        return self.text[:7]
    