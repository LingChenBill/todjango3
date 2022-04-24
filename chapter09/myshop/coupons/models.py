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
