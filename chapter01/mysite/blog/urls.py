#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/3/26
# @Author: Lingchen
# @Prescription:
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post列表页面.
    path('', views.post_list, name='post_list'),
    # post详细页面.
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
]
