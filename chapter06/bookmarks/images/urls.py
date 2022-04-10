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
    # 图片喜欢操作.
    path('like/', views.image_like, name='like'),
    # 图片列表.
    path('', views.image_list, name='list'),
    # 图片排名.
    path('ranking/', views.image_ranking, name='ranking'),
]
