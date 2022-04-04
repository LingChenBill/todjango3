#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/4
# @Author: Lingchen
# @Prescription:
from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    自定义认证后台.
    一个简单的身份验证后端.
    authenticate()方法接收请求对象以及用户名和密码可选参数.
    您可以使用不同的参数，但您可以使用用户名和密码使后端立即与身份验证框架视图一起工作.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            # 检索具有给定电子邮件地址的用户.
            user = User.objects.get(email=username)
            # 并使用用户模型的内置check_password（）方法检查密码.
            # 此方法处理密码散列，以将给定密码与存储在数据库中的密码进行比较.
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
