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


# class User(AbstractBaseUser, PermissionsMixin):
#     """
#     An abstract base class implementing a fully featured User model with
#     admin-compliant permissions.

#     Username and password are required. Other fields are optional.
#     """

#     username_validator = UnicodeUsernameValidator()

#     username = models.CharField(
#         ("username"),
#         max_length=150,
#         unique=True,
#         help_text=(
#             "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
#         ),
#         validators=[username_validator],
#         error_messages={
#             "unique": ("A user with that username already exists."),
#         },
#     )
#     first_name = models.CharField(("first name"), max_length=150, blank=True)
#     last_name = models.CharField(("last name"), max_length=150, blank=True)
#     email = models.EmailField(("email address"), blank=True)
#     is_staff = models.BooleanField(
#         ("staff status"),
#         default=False,
#         help_text=("Designates whether the user can log into this admin site."),
#     )
#     is_active = models.BooleanField(
#         ("active"),
#         default=True,
#         help_text=(
#             "Designates whether this user should be treated as active. "
#             "Unselect this instead of deleting accounts."
#         ),
#     )
#     date_joined = models.DateTimeField(("date joined"), default=timezone.now)

#     objects = UserManager()

#     EMAIL_FIELD = "email"
#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["email"]

#     class Meta:
#         verbose_name = ("user")
#         verbose_name_plural = ("users")
#         abstract = True

#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)

#     def get_full_name(self):
#         """
#         Return the first_name plus the last_name, with a space in between.
#         """
#         full_name = "%s %s" % (self.first_name, self.last_name)
#         return full_name.strip()

#     def get_short_name(self):
#         """Return the short name for the user."""
#         return self.first_name

#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Send an email to this user."""
#         send_mail(subject, message, from_email, [self.email], **kwargs)