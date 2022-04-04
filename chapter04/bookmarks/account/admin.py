from django.contrib import admin
from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    profile配置.
    """
    list_display = ['user', 'date_of_birth', 'photo']
