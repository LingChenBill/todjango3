#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/12
# @Author: Lingchen
# @Prescription:
from django import forms
from django.utils.translation import gettext_lazy as _

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """
    允许用户选择数量.
    """
    # 这允许用户选择1到20之间的数量. 使用coerce=int的TypedChoiceField字段将输入转换为整数.
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,
                                      label=_('Quantity'))
    # 说明是否必须添加数量到此产品的购物车中的任何现有数量(False), 或是否必须用给定数量覆盖现有数量(True).
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)

