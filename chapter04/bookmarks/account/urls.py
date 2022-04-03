#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/2
# @Author: Lingchen
# @Prescription:
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # login.
    # path('login/', views.user_login, name='login'),
    # 配置用户登录的dashboard url.
    path('', views.dashboard, name='dashboard'),
    # auth class-based login views.
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 密码修改urls.
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
