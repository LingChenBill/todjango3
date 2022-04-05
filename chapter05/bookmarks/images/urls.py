#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/5
# @Author: Lingchen
# @Prescription:
from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    # 图片创建.
    path('create/', views.image_create, name='create'),
]
