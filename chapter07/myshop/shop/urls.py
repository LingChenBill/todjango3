#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/11
# @Author: Lingchen
# @Prescription:
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # 商品列表页面.
    path('', views.product_list, name='product_list'),
    # 以商品类别显示商品列表.
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    # 商品详细.
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
