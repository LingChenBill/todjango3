#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/2
# @Author: Lingchen
# @Prescription:
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """
    用户登录form.
    """
    username = forms.CharField()
    # input -> password type.
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """
    用户注册form.
    """
    # 添加表单的项目.
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        # 表单的元素.
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """
        对照第一个密码检查第二个密码，如果密码不匹配，不让表单is_valid()验证通过.
        当您通过调用表单的is_valid（）方法验证表单时，将完成此检查.
        :return:
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match. ')
        return cd['password2']
