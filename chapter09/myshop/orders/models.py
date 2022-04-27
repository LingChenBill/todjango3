from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Order(models.Model):
    """
    订单模型包含几个用于存储客户信息的field和一个默认为False的付费布尔field.
    稍后，您将使用此字段来区分已付款订单和未付款订单.
    """
    first_name = models.CharField(_('first_name'), max_length=50)
    last_name = models.CharField(_('last_name'), max_length=50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'), max_length=250)
    postal_code = models.CharField(_('postal_code'), max_length=20)
    city = models.CharField(_('city'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)

    # braintree的沙箱交易id.
    braintree_id = models.CharField(max_length=150, blank=True)

    # 存储订单的可选优惠券以及优惠券应用的折扣百分比.
    # 折扣存储在相关优惠券对象中，但如果优惠券被修改或删除，可以将其包括在订单模型中以保留折扣.
    # 设置了on_delete = SET_NULL, 这样如果优惠券被删除，优惠券字段将设置为NULL，但折扣将保留.
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    # order中保留折扣.
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        """
        获取此订单中购买的物品的总成本.
        :return:
        """
        # return sum(item.get_cost() for item in self.items.all())
        # 总价 - 折扣价.
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))


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
