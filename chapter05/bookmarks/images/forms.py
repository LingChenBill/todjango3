#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/5
# @Author: Lingchen
# @Prescription:
from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):
    """
    图片创建form.
    此表单是基于图像模型构建的模型表单，仅包括标题、url和描述.
    用户不会直接在表单中输入图像URL.
    相反，您将为他们提供一个JavaScript工具，用于从外部站点选择图像，您的表单将接收其URL作为参数.
    可以覆盖url字段的默认小部件，以使用HiddenInput小部件.
    """
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

        # 此widgets小部件呈现为带有type=“hidden”属性的HTML输入元素.
        # 你使用这个小部件是因为你不想让用户看到这个字段.
        widgets = {
            'url': forms.HiddenInput,
        }

        def clean_url(self):
            """
            拆分URL以获取file扩展名，并检查它是否为有效的扩展名.
            如果扩展无效，则引发ValidationError并表单实例将不会被验证.
            :return:
            """
            url = self.cleaned_data['url']
            valid_extensions = ['jpg', 'jpeg']
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('The given URL does not match valid image extensions.')
            return url
