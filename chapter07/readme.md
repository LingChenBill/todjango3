####1.创建工程
```bash
django-admin startproject myshop

django-admin startapp shop
```
`settings.py`:
```python
'shop.apps.ShopConfig',
```
####2.创建models.
`models.py`中, 创建`Category`和`Product`模型. 图片处理, 安装依赖:
```bash
pip install Pillow
```
数据迁移:
```bash
python manage.py makemigrations

python manage.py migrate
```
####3.将model添加到管理中.
`admin.py`:
```python
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
```
创建超级用户:
```bash
python manage.py createsuperuser

lingchen
admin

python manage.py runserver

http://localhost:8000/admin

添加商品类别和商品.
```
####4.图片配置.
在`settings.py`中配置图片路径:
```python
import os

# 图片路径配置.
# MEDIA_URL是为用户上传的媒体文件提供服务的基本URL.
# MEDIA_ROOT是这些文件所在的本地路径，您可以通过动态预加BASE_DIR变量来构建它.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```
在`urls.py`中配置图片路径:
```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
```
####5.页面templates:
```html
chapter07/myshop/shop/templates/shop/product/detail.html
chapter07/myshop/shop/templates/shop/product/list.html
chapter07/myshop/shop/templates/shop/base.html
```
静态文件css:
```text
chapter07/myshop/shop/static/css/base.css
```
####6.url的path配置:
`chapter07/myshop/shop/urls.py`:
```python
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # 商品列表页面.
    path('', views.product_list, name='product_list'),
    # 以商品类别显示商品列表.
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # 商品详细.
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
```
####7.在网页中验证:
```text
http://localhost:8000/
```
