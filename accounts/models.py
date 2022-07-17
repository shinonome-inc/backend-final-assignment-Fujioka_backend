from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class FollowModel(models.Model):
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='following_user')
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='follower_user')
