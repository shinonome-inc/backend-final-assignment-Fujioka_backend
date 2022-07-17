from django.contrib import admin
from .models import LikeModel, TweetModel

# Register your models here.

admin.site.register(TweetModel)
admin.site.register(LikeModel)
