####1.创建braintreegateway sandbox注册账号.
```text
https://www. braintreepayments.com/sandbox
```
安装braintree支付网关的依赖:
```bash
pip install braintree
```
创建payment app:
```bash
python manage.py startapp payment
```
配置app, `chapter08/myshop/myshop/settings.py`:
```python
'payment.apps.PaymentConfig',

# braintree config.
BRAINTREE_MERCHANT_ID = 'xxxx'
BRAINTREE_PUBLIC_KEY = 'xxxx'
BRAINTREE_PRIVATE_KEY = 'xxxx'

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)
```
订单创建后, 重定向到payment, `chapter08/myshop/orders/views.py`:
```python
from django.shortcuts import render, redirect
from django.urls import reverse

# 发布异步任务.
order_created.delay(order.id)

# 将订单id存入session.
request.session['order_id'] = order_id
# 重定向到payment.
# return redirect(reverse('payment:process'))
```
将order订单与交易id关联, `chapter08/myshop/orders/models.py`:
```python
# braintree的沙箱交易id.
braintree_id = models.CharField(max_length=150, blank=True)
```
数据迁移:
```bash
python manage.py makemigrations

python manage.py migrate
```
创建view, `chapter08/myshop/payment/views.py`:
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
import braintree

# Create your views here.

# 实例化braintree的网关.
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    """
    支付流程.
    :param request:
    :return:
    """
    order_id = request.session.get('order_id')

    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # 取回付款方法.
        nonce = request.POST.get('payment_method_nonce', None)
        result = gateway.transaction.sale({
            'amount': f'{total_cost: .2f}',
            'payment_method_nonce': nonce,
            'options': {
                # 发送带有True的submit_for_settlement选项, 这样交易就会自动提交进行结算.
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            # 更新订单支付状态.
            order.paid = True
            # 保存交易id.
            order.braintree_id = result.transaction.id
            order.save()

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        client_token = gateway.client_token.generate()

        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    """
    支付完成.
    :param request:
    :return:
    """
    return render(request, 'payment/done.html')


def payment_canceled(request):
    """
    支付取消.
    :param request:
    :return:
    """
    return render(request, 'payment/canceled.html')
```
配置url, `chapter08/myshop/payment/urls.py`:
```python
from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # 交易支付url.
    path('process/', views.payment_process, name='process'),
    # 支付完成url.
    path('done/', views.payment_done, name='done'),
    # 支付取消url.
    path('canceled/', views.payment_canceled, name='canceled'),
]
```
将payment urls加入到整个app的urls,`chapter08/myshop/myshop/urls.py`:
```python
# 交易urls.
path('payment', include('payment.urls', namespace='payment')),
```
创建templates:
```text
chapter08/myshop/payment/templates/payment/canceled.html
chapter08/myshop/payment/templates/payment/done.html
chapter08/myshop/payment/templates/payment/process.html
```
验证, 在商品页面,调整商品价格:
```text
celery -A myshop worker -l info

python manage.py runserver

http://localhost:8000/admin/shop/product/

交易test号:
https://developer.paypal.com/braintree/docs/reference/general/testing/#test-value-4111111111111111

https://sandbox.braintreegateway.com/merchants/j47ygk4dfffnfnmz/transactions/advanced_search
```
在订单生成后, 可以在orders_order表中, 可以看到沙箱中生成的交易id.
