from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'following', 'following_number']


admin.site.register(User, CustomUserAdmin)

