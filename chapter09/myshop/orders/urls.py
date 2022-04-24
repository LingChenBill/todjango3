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
    # 自定制order管理页面.
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    # pdf导出.
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
]
