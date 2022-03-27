#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/3/27
# @Author: Lingchen
# @Prescription:
from django import forms


class EmailPostForm(forms.Form):
    """
    创建email的提交表单.
    """
    # CharField -> input text.
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # CharField + widget -> input textarea.
    comments = forms.CharField(required=False, widget=forms.Textarea)
