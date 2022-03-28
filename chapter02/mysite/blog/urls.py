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
    # 使用基于类的对象视图.
    # path('', views.PostListView.as_view(), name='post_list'),
    # post详细页面.
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    # 邮件.
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    # 查询带tag的post的列表.
    # slug path转换器，将参数匹配为带有ASCII字母或数字的小写字符串，再加上连字符和下划线字符.
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
]
