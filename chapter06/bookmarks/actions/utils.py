#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/10
# @Author: Lingchen
# @Prescription:
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    """
    创建action.
    允许您创建可选包含目标对象的操作.
    您可以在代码中的任何位置使用此函数作为向活动流添加新操作的快捷方式.
    :param user:
    :param verb:
    :param target:
    :return:
    """
    action = Action(user=user, verb=verb, target=target)
    action.save()

