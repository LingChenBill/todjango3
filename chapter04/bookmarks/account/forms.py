#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/2
# @Author: Lingchen
# @Prescription:
from django import forms


class LoginForm(forms.Form):
    """
    用户登录form.
    """
    username = forms.CharField()
    # input -> password type.
    password = forms.CharField(widget=forms.PasswordInput)
