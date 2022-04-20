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
####2.导出csv.
在admin的order列表中加入一个导出csv的功能. `chapter08/myshop/orders/admin.py`:
```python
from django.http import HttpResponse
import csv
import datetime


def export_to_csv(modeladmin, request, queryset):
    """
    csv导出.
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    # 创建一个HttpResponse实例，指定text/csv内容
    # 浏览器响应必须被视为CSV文件. 可以添加一个内容处置头，以指示HTTP响应包含附加的file.
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    # 创建将写入响应对象的CSV编写器对象.
    writer = csv.writer(response)

    # 可以使用get_fields()方法动态获取模型field模型的meta选项. 排除多对多和一对多关系.
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # 标题行.
    writer.writerow([field.verbose_name for field in fields])

    # 迭代给定的查询集，并为返回的每个对象写一行在QuerySet.
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            # 因为CSV的输出值必须是字符串，所以需要设置datetime对象的格式.
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')

            data_row.append(value)
        writer.writerow(data_row)

    return response
# 在"操作"下拉列表中自定义操作的显示名称通过在函数上设置short_description属性来创建管理站点的元素.
export_to_csv.short_description = 'Export to CSV'


# 将export_to_csv管理操作添加到OrderAdmin类.
actions = [export_to_csv]
```
在浏览器中验证:
```text
http://localhost:8000/admin/orders/order/
```
官网csv输出实例:
```text
https://docs.djangoproject.com/en/3.0/howto/outputting-csv/
```
####3.定制管理页面的订单view画面
`chapter08/myshop/orders/views.py`:
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def admin_order_detail(request, order_id):
    """
    定制管理页面的订单详细页面.
    staff_member_required decorator检查请求页面的用户的is_active和is_staff field是否都设置为True.
    在这个视图中，将获得具有给定ID的Order对象，并呈现一个模板来显示订单.
    :param request:
    :param order_id:
    :return:
    """
    order = get_object_or_404(Order, id=order_id)

    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

```
配置url,`chapter08/myshop/orders/urls.py`:
```python
# 自定制order管理页面.
path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
```
管理页面,`chapter08/myshop/orders/admin.py`:
```python
from django.urls import reverse
from django.utils.safestring import mark_safe


def order_detail(obj):
    """
    定制管理页面的订单详细页面.
    将Order对象作为参数，并返回admin_Order_detail URL的HTML链接.
    默认情况下，Django转义HTML输出.必须使用mark_safe功能以避免自动逃逸.
    :param obj:
    :return:
    """
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                    'city', 'paid', 'created', 'updated',
                    order_detail]
```
template创建, `chapter08/myshop/orders/templates/admin/orders/order/detail.html`. 网页验证:
```text
http://localhost:8000/admin/orders/order/
```
####4.安装pdf导出依赖
```bash
pip install WeasyPrint
```
创建pdf的templates, `chapter08/myshop/orders/templates/orders/order/pdf.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My shop</title>
</head>
<body>
  <h1>My shop</h1>
  <p>
    Invoice no. {{ order.id }}<br />
    <span class="secondary">
      {{ order.created|date:'Y/m/d' }}
    </span>
  </p>

  <h3>Bil to</h3>
  <p>
    {{ order.first_name }} {{ order.last_name }}<br />
    {{ order.email }}<br />
    {{ order.address }}<br />
    {{ order.postal_code }}, {{ order.city }}
  </p>

  <h3>Items brought</h3>
  <table>
    <thead>
      <tr>
        <th>Product</th>
        <th>Price</th>
        <th>Quantity</th>
        <th>Cost</th>
      </tr>
    </thead>
    <tbody>
      {% for item in order.items.all %}
        <tr class="row{% cycle '1' '2' %}">
          <td>{{ item.product.name }}</td>
          <td class="num">{{ item.price }}</td>
          <td class="num">{{ item.quantity }}</td>
          <td class="num">{{ item.get_cost }}</td>
        </tr>
      {% endfor %}
      <tr class="total">
        <td colspan="3">Total</td>
        <td class="num">{{ order.get_total_cost }}</td>
      </tr>
    </tbody>
  </table>

  <span class="{% if order.paid %}paid{% else %}pending{% endif %}">
    {% if order.paid %}Paid{% else %}Pending payment{% endif %}
  </span>
</body>
</html>
```
编写view, `chapter08/myshop/orders/views.py`:
```python
import weasyprint

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


@staff_member_required
def admin_order_pdf(request, order_id):
    """
    打印PDF.
    :param request:
    :param order_id:
    :return:
    """
    # 获取具有给定ID的Order对象，然后使用Django提供的render_to_string()函数来呈现orders/Order/pdf.html.
    # 呈现的HTML保存在HTML变量中.
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{ order.id}.pdf'

    # 使用WeasyPrint从呈现的HTML代码生成PDF文件，并将该文件写入HttpResponse对象.
    # 使用静态file css/pdf.css将css样式添加到生成的PDF文件中.
    # 然后，使用STATIC_ROOT设置从本地路径加载它. 最后，返回生成的response.
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + 'css/pdf.css')])
    return response
```
创建pdf的css, `chapter08/myshop/shop/static/css/pdf.css`:
```css
body {
    font-family:Helvetica, sans-serif;
    color:#222;
    line-height:1.5;
}

table {
    width:100%;
    border-spacing:0;
    border-collapse: collapse;
    margin:20px 0;
}

table th, table td {
    text-align:left;
    font-size:14px;
    padding:10px;
    margin:0;
}

tbody tr:nth-child(odd) {
    background:#efefef;
}

thead th, tbody tr.total {
    background:#5993bb;
    color:#fff;
    font-weight:bold;
}

h1 {
    margin:0;
}


.secondary {
    color:#bbb;
    margin-bottom:20px;
}

.num {
    text-align:right;
}

.paid, .pending {
    color:#1bae37;
    border:4px solid #1bae37;
    text-transform:uppercase;
    font-weight:bold;
    font-size:22px;
    padding:4px 12px 0px;
    float:right;
    transform: rotate(-15deg);
    margin-right:40px;
}

.pending {
    color:#a82d2d;
    border:4px solid #a82d2d;
}
```
配置`settings.py`:
```python
# PDF conf.
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```
生成PDF的相关static的相关文件:
```bash
python manage.py collectstatic
```
配置url, `chapter08/myshop/orders/urls.py`:
```python
# pdf导出.
path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
```
将pdf加入管理页面中, `chapter08/myshop/orders/admin.py`:
```python
def order_pdf(obj):
    """
    pdf导出.
    :param obj:
    :return:
    """
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                    'city', 'paid', 'created', 'updated',
                    order_detail,
                    order_pdf]
```
在页面验证:
```bash
python manage.py runserver
```
html:
```text
http://127.0.0.1:8000/admin/orders/order/
```



