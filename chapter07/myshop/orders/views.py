from django.shortcuts import render
from .models import OrderItem
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

            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
