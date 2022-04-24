from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


# Create your views here.


@require_POST
def coupon_apply(request):
    """
    折扣编辑应用.
    :param request:
    :return:
    """
    now = timezone.now()
    form = CouponApplyForm(request.POST)

    if form.is_valid():
        code = form.cleaned_data['code']

        try:
            # 使用iexact字段查找来执行不区分大小写的查询完全匹配.
            # 优惠券必须当前处于活动状态（活动=真）且有效对于当前日期时间.
            # 你使用Django的时区函数来获取当前时区感知日期时间，并将其与有效日期时间进行比较_lte（小于或等于）和gte（大于或等于）字段查找.
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)

            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('cart:cart_detail')
