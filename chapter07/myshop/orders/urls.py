#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/13
# @Author: Lingchen
# @Prescription:
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # 订单创建.
    path('create/', views.order_create, name='order_create'),
]
