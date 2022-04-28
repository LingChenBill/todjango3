#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/16
# @Author: Lingchen
# @Prescription:
from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

app_name = 'payment'

urlpatterns = [
    # 交易支付url.
    path(_('process/'), views.payment_process, name='process'),
    # 支付完成url.
    path(_('done/'), views.payment_done, name='done'),
    # 支付取消url.
    path(_('canceled/'), views.payment_canceled, name='canceled'),
]
