#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/2
# @Author: Lingchen
# @Prescription:
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # login.
    # path('login/', views.user_login, name='login'),
    # 配置用户登录的dashboard url.
    path('', views.dashboard, name='dashboard'),

    # # auth class-based login views.
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # # 密码修改urls.
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # # 重置密码urls.
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # 上述auth中的class-based views的url的缩写.
    path('', include('django.contrib.auth.urls')),

    # 用户注册.
    path('register/', views.register, name='register'),
]
