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
