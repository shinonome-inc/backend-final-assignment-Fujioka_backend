from tkinter import CASCADE
from django.db import models
from django.utils import timezone

from accounts.models import User


class TweetModel(models.Model):
    text = models.TextField(max_length=140)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text[:7]

# 今後の拡張性の確保のため別のテーブルを作成した
class LikeModel(models.Model):
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)

# modelの対応関係は、User-Tweet(1-n), Tweet-Like(1-n)
# 依存関係：Tweet(User), Like(Tweet, User)
