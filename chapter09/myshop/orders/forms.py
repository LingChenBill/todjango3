#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/13
# @Author: Lingchen
# @Prescription:
from django import forms
from localflavor.us.forms import USZipCodeField
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
    订单创建表单.
    """
    # 美国邮政编码字段，以便创建新订单时需要有效的美国邮政编码.
    postal_code = USZipCodeField()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
