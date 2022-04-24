#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/14
# @Author: Lingchen
# @Prescription:
import os
from celery import Celery

# 为celery程序设置默认的Django设置模块.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

# 使用创建应用程序的实例.
app = Celery('myshop')

# namespace属性指定celery相关设置在设置中的settings.py文件.
# 通过设置Celery名称空间，所有芹菜设置都需要包含celery名称中的前缀(例如CELERY_BROKER_URL).
app.config_from_object('django.conf:settings', namespace='CELERY')

# celery会寻找一种tasks.py文件为加载而添加到INSTALLED_APPS的异步任务.
# 其中定义的异步任务。
app.autodiscover_tasks()
