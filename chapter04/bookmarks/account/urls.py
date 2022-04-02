#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/2
# @Author: Lingchen
# @Prescription:
from django.urls import path
from . import views

urlpatterns = [
    # login.
    path('login/', views.user_login, name='login'),
]
