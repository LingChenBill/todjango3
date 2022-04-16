#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/13
# @Author: Lingchen
# @Prescription:
from .cart import Cart


def cart(request):
    """
    在上下文处理器中，使用请求对象实例化cart，并将其作为名为cart的变量用于模板.
    :param request:
    :return:
    """
    return {'cart': Cart(request)}
