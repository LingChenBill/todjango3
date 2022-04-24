import weasyprint
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


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

            # 发布异步任务.
            order_created.delay(order.id)

            # 将订单id存入session.
            request.session['order_id'] = order.id
            # 重定向到payment.
            return redirect(reverse('payment:process'))

            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})
    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


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
