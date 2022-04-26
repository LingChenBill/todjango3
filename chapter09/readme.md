####1.创建折扣app.
```bash
python manage.py startapp coupons
```
将app添加到主工程中, `chapter09/myshop/myshop/settings.py`
```python
'coupons.apps.CouponsConfig',
```
创建折扣model, `chapter09/myshop/coupons/models.py`:
```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Coupon(models.Model):
    """
    折扣model.
    """
    # 用户必须输入的代码，以便将优惠券应用于他们的帐户购买.
    code = models.CharField(max_length=50, unique=True)
    # 指示优惠券何时到期的日期时间值有效的.
    valid_from = models.DateTimeField()
    # 指示优惠券何时到期的日期时间值无效的.
    valid_to = models.DateTimeField()

    # 要应用的折扣率（这是一个百分比，因此它需要值, 从0到100). 使用此字段的验证器来限制最小值和最大可接受值.
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    # 指示优惠券是否处于活动状态的布尔值.
    active = models.BooleanField()

    def __str__(self):
        return self.code
```
数据迁移入DB:
```bash
python manage.py makemigrations

python manage.py migrate
```
修改文件:
```text
chapter09/myshop/myshop/urls.py
chapter09/myshop/cart/views.py
chapter09/myshop/cart/cart.py
chapter09/myshop/coupons/admin.py
chapter09/myshop/coupons/apps.py
chapter09/myshop/coupons/forms.py
chapter09/myshop/coupons/models.py
chapter09/myshop/coupons/tests.py
chapter09/myshop/coupons/urls.py
chapter09/myshop/coupons/views.py
```
修改templates:
```text
chapter09/myshop/orders/templates/orders/order/create.html
chapter09/myshop/cart/templates/cart/detail.html
```
