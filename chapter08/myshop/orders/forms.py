#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/13
# @Author: Lingchen
# @Prescription:
from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
    订单创建表单.
    """
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
