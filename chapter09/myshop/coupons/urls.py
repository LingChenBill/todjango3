#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/24
# @Author: Lingchen
# @Prescription:
from django.urls import path
from . import views

app_name = 'coupons'

urlpatterns = [
    # code url.
    path('apply/', views.coupon_apply, name='apply'),
]
