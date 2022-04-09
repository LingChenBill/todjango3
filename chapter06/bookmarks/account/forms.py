#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/2
# @Author: Lingchen
# @Prescription:
from django import forms
from django.contrib.auth.models import User
from .models import Profile


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


class UserEditForm(forms.ModelForm):
    """
    用户编辑form.
    这将允许用户编辑他们的名字，姓氏，和电子邮件，这是内置Django用户模型的属性.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """
    用户profile编辑form.
    允许用户编辑您需要的配置文件数据保存在自定义配置文件模型中.
    用户可以编辑他们的注册日期出生并上传他们个人资料的图片.
    """
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
