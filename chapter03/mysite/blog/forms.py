#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/3/27
# @Author: Lingchen
# @Prescription:
from django import forms
from .models import Comment


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


class CommentForm(forms.ModelForm):
    """
    根据Model:Comment来创建一个动态的Form.
    """
    class Meta:
        model = Comment
        # 表单元素的限定.
        fields = ('name', 'email', 'body')
