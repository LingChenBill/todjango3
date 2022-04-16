from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
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
