from django.contrib import admin
from .models import Action

# Register your models here.


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    """
    将Action注册到admin管理中.
    """
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)
