from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


# Create your views here.


def product_list(request, category_slug=None):
    """
    获取商品列表.
    :param request:
    :param category_slug:
    :return:
    """
    category = None
    categories = Category.objects.all()
    # 使用available=True筛选QuerySet以仅检索可用产品.
    products = Product.objects.filter(available=True)

    if category_slug:
        # 使用可选的category_slug参数，可以根据给定的类别选择性过滤产品.
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


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
    # product = get_object_or_404(Product, id=id, slug=slug, available=True)
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)

    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
