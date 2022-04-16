#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/16
# @Author: Lingchen
# @Prescription:
from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    # 交易支付url.
    path('process/', views.payment_process, name='process'),
    # 支付完成url.
    path('done/', views.payment_done, name='done'),
    # 支付取消url.
    path('canceled/', views.payment_canceled, name='canceled'),
]
