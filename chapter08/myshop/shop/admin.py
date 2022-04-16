from django.contrib import admin
from .models import Category, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    类别管理.
    """
    list_display = ['name', 'slug']
    # prepopulated_fields属性指定使用其他FIELD的值自动设置值的FIELD.
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    商品管理.
    """
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']

    # 使用ProductAdmin类中的list_editable属性设置可以从管理网站的list display页面编辑的FIELD.
    # list_editable中的任何字段也必须在list_display中列出，因为只有显示的字段可以编辑.
    list_editable = ['price', 'available']

    prepopulated_fields = {'slug': ('name',)}
