from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.


@require_POST
def cart_add(request, product_id):
    """
    将产品添加到购物车或更新现有产品的数量.
    :param request:
    :param product_id:
    :return:
    """
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    # 获取post方式中的数据form.
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        # 添加或者更新购物车中的商品.
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    删除购物车中的商品.
    :param request: 
    :param product_id: 
    :return: 
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect('cart:cart_detail')


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
