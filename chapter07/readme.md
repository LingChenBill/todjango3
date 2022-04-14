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
####10.更新购物车中的数量.
`views.py`:
```python
def cart_detail(request):
    """
    显示购物车商品信息.
    :param request:
    :return:
    """
    cart = Cart(request)

    # 为购物车中的每个商品创建CartAddProductForm实例，以允许更改产品数量.
    # 使用当前物料数量初始化表单，并将覆盖字段设置为True，这样当您将表单提交到cart_add视图时，当前数量将替换为新数量.
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})

    return render(request,
                  'cart/detail.html',
                  {'cart': cart})
```
修改templates的`cart/detail.html`:
```html
<!--{{ item.quantity }}-->
<form action="{% url 'cart:cart_add' product.id %}" method="post">
  {{ item.update_quantity_form.quantity }}
  {{ item.update_quantity_form.override }}
  {% csrf_token %}
  <input type="submit" value="Update" />
</form>
```
####11.创建购物车的上下文.创建`context_processors.py`:
```python
from .cart import Cart


def cart(request):
    """
    在上下文处理器中，使用请求对象实例化cart，并将其作为名为cart的变量用于模板.
    :param request:
    :return:
    """
    return {'cart': Cart(request)}
```
配置`settings.py`:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]
```
修改`base.html`:
```html
<div id="subheader">
  <div class="cart">
    {% with total_items=cart|length %}
      {% if total_items > 0 %}
        Your cart:
        <a href="{% url 'cart:cart_detail' %}">
          {{ total_items }} item{{ total_items | pluralize }}, ¥{{ cart.get_total_price }}
        </a>
      {% else %}
        Your cart is empty.
      {% endif %}
    {% endwith %}
  </div>
</div>
```
####12.创建订单app,orders
```bash
python manage.py startapp orders
```
创建订单model:
```python
from django.db import models
from shop.models import Product

# Create your models here.


class Order(models.Model):
    """
    订单模型包含几个用于存储客户信息的field和一个默认为False的付费布尔field.
    稍后，您将使用此字段来区分已付款订单和未付款订单.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        """
        获取此订单中购买的物品的总成本.
        :return:
        """
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """
    储存每件商品的产品、数量和价格.
    """
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)

    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """
        获取商品的价格.
        :return:
        """
        return self.price * self.quantity
```
数据迁移:
```bash
python manage.py makemigrations

python manage.py migrate
```
####13.将order model加入到管理页面, `admin.py`:
```python
from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    """
    使用OrderItem模型的ModelInline类将其作为内联包含在OrderAdmin类中.
    内联允许您在与其相关模型相同的编辑页面上包含模型.
    """
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                    'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']

    inlines = [OrderItemInline]
```
在网页中验证:
```bash
python manage.py runserver

http://127.0.0.1:8000/admin/orders/order/add/
```
####14.创建订单view url:
```python
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

# Create your views here.


def order_create(request):
    """
    创建订单.
    :param request:
    :return:
    """
    # 使用cart=cart(request)从会话中获取当前购物车.
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # 清空购物车.
            cart.clear()

            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
```
`urls.py`:
```python
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # 订单创建.
    path('create/', views.order_create, name='order_create'),
]
```
`chapter07/myshop/myshop/urls.py`:
```python
# 订单urls.
path('orders/', include('orders.urls', namespace='orders')),
```
创建templates:
```text
chapter07/myshop/orders/templates/orders/order/create.html
chapter07/myshop/orders/templates/orders/order/created.html
```
####15.安装异步队列celery
```bash
pip install celery
```
配置celery, `chapter07/myshop/myshop/celery.py`:
```python
import os
from celery import Celery

# 为celery程序设置默认的Django设置模块.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

# 使用创建应用程序的实例.
app = Celery('myshop')

# namespace属性指定celery相关设置在设置中的settings.py文件.
# 通过设置Celery名称空间，所有芹菜设置都需要包含celery名称中的前缀(例如CELERY_BROKER_URL).
app.config_from_object('django.conf:settings', namespace='CELERY')

# celery会寻找一种tasks.py文件为加载而添加到INSTALLED_APPS的异步任务.
# 其中定义的异步任务。
app.autodiscover_tasks()
```
在django启动时, 加载celery, `chapter07/myshop/myshop/__init__.py`:
```python
# 程序启动时, 加载celery.
from .celery import app as celery_app
```
创建`chapter07/myshop/orders/tasks.py`:
```python
from myshop.celery import app
from django.core.mail import send_mail
from .models import Order


@app.task
def order_created(order_id):
    """
    订单异步任务创建.
    celery任务只是一个用@task修饰的Python函数.任务函数接收订单id参数.
    始终建议在执行任务时仅将ID传递给任务函数和查找对象.
    可以使用Django提供的send_mail()函数向下订单的用户发送电子邮件通知.
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order_id}'

    message = f'Dear {order.first_name}, \n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order_id}.'

    mail_sent = send_mail(subject,
                          message,
                          'lingchen1316@163.com',
                          [order.email])
    return mail_sent
```
在`chapter07/myshop/myshop/settings.py`中, 配置email的控制台输出:
```python
# email console配置.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
在订单创建中, 添加异步任务``:
```python
from .tasks import order_created

# 发布异步任务.
order_created.delay(order.id)
```
docker中启动rabbitMQ:
```bash
% docker start 856
856
% docker ps
CONTAINER ID   IMAGE                       COMMAND                  CREATED         STATUS         PORTS                                                                                                         NAMES
8565ee9b241b   rabbitmq:3.8.9-management   "docker-entrypoint.s…"   17 months ago   Up 2 seconds   4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, 15671/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp   affectionate_lumiere
```
启动app:
```bash
python manage.py runserver

# 启动celery
celery -A myshop worker -l info
```
可以浏览器中, 查看rabbitMQ的管理页面:
```text
http://localhost:15672/

guest
guest
```
在`localhost:8000`中, 创建order订单, checkout后, 可以在控制台, 查看异步任务, email输出.

####16.监控celery, 安装依赖:
```bash
pip install flower
```
启动工程, 和celery:
```bash
python manage.py runserver

celery -A myshop worker -l info

celery -A myshop flower
```
在flower的管理页面, 查看flower监控的celery情况:
```text
http://localhost:5555/
```
