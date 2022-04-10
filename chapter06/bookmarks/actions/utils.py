#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/10
# @Author: Lingchen
# @Prescription:
import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    """
    创建action.
    允许您创建可选包含目标对象的操作.
    您可以在代码中的任何位置使用此函数作为向活动流添加新操作的快捷方式.
    避免保存重复的操作，并返回布尔值来告诉您是否保存了该操作.
    :param user:
    :param verb:
    :param target:
    :return:
    """
    now = timezone.now()

    # 使用last_minute变量存储一分钟后的日期时间并检索用户此后执行的任何相同操作.
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False


