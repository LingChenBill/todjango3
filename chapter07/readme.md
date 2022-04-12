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

####8.创建购物车cart app.
```bash
python manage.py startapp cart
```
将cart app加入到apps的`settings.py`中:
```python
'cart.apps.CartConfig',

# 购物车session key.
# 将购物车存储在用户会话中. 由于Django会话是按访客管理的，因此可以对所有会话使用相同的购物车会话密钥.
CART_SESSION_ID = 'cart'
```
####9.新建购物车的操作类.
`cart.py`:
```python
from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    xxxxxx
```

新建购物车相关的views, urls:
```text
chapter07/myshop/cart/urls.py
chapter07/myshop/cart/views.py
```
购物车的detail页面:
```text
chapter07/myshop/cart/templates/cart/detail.html
```
更新shop的urls, 包括购物车的urls:
```text
chapter07/myshop/myshop/urls.py

# 商品urls.
path('', include('shop.urls', namespace='shop')),
```
更新商品的detail的views:
```python
def product_detail(request, id, slug):
    """
    商品详细页面.
    id和slug参数以检索产品实例.
    :param request:
    :param id:
    :param slug:
    :return:
    """
    # 仅通过ID获取此实例，因为它是唯一的属性. 但是，您可以在URL中包含slug，以便为产品构建SEO友好的URL.
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
```
