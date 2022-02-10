from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Profile

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'user_name', ]

admin.site.register(CustomUser)
admin.site.register(Profile)
