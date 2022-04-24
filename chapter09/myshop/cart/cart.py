#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/12
# @Author: Lingchen
# @Prescription:
from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart(object):
    """
    管理购物车, 您需要使用请求对象初始化购物车.
    """
    def __init__(self, request):
        # 使用self.session存储当前会话request.session.使Cart类的其他方法可以访问它.
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 赋于一个空的cart到session中.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # 将折扣ID存入session.
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        """
        将商品加入购物车或更新已在购物车中的商品数量.
        :param product: 要在购物车中添加或更新的产品实例.
        :param quantity: 带有产品数量的可选整数. 默认值为1.
        :param override_quantity: 商品数量是添加还是更新(累加).
        :return:
        """
        # 将产品ID转换为字符串，因为Django使用JSON序列化会话数据，而JSON只允许使用字符串键名.
        product_id = str(product.id)
        if product_id not in self.cart:
            # 产品ID是key，而您要保留的值是一个包含产品数量和价格信息的字典.
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        将会话标记为“已修改”，以确保其已保存.
        :return:
        """
        self.session.modified = True

    def remove(self, product):
        """
        删除session中的商品.
        :param product:
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            # 删除商品id对应的商品.
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        迭代购物车中的项目，并从数据库中获取产品.
        :return:
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        # 在cart变量中复制当前购物车，并将产品实例添加到其中.
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        购物车的商品数量.
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        返回购物车中的商品总价.
        :return:
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        清空购物车.
        :return:
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """
        折扣处理.
        将此方法定义为属性. 如果购物车包含优惠券id属性，返回具有给定id的优惠券对象.
        :return:
        """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """
        获取折扣.
        如果购物车包含优惠券，则可以检索其折扣对要从购物车总金额中扣除的金额进行评级并返还.
        :return:
        """
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()

        return Decimal(0)

    def get_total_price_after_discount(self):
        """
        返回所需的总金额扣除get_discount()方法返回的金额后的购物车.
        :return:
        """
        return self.get_total_price() - self.get_discount()

