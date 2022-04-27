#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/24
# @Author: Lingchen
# @Prescription:
from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    """
    折扣form.
    """
    code = forms.CharField(label=_('Coupon'))
