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
    # 图片详细信息.
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
]
