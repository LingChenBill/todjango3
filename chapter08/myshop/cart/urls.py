#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/12
# @Author: Lingchen
# @Prescription:
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # 购物车url.
    path('', views.cart_detail, name='cart_detail'),
    # 添加商品到购物车.
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    # 删除购物车中商品.
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
