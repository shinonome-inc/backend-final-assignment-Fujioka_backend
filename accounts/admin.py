from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    # fieldsets = User.fieldsets + ((None, {'fields': ('following', 'following_number')}),)
    list_display = ['username', 'following', 'following_number']


admin.site.register(User, CustomUserAdmin)