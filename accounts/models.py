from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail


class User(AbstractUser):

    following = models.TextField(null=True, blank=True, default='')
    follower = models.TextField(null=True, blank=True, default='')
    following_number = models.IntegerField(null=True, blank=True, default=0)
    follower_number = models.IntegerField(null=True, blank=True, default=0)
    
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

class FriendShip(models.Model):
    pass

