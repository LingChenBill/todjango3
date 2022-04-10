#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/10
# @Author: Lingchen
# @Prescription:
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    """
    使用receiver() decorator将users_like_changed函数注册为receiver函数, 将其连接到m2m_changed.
    然后，将函数连接到Image.users_like. 通过，以便仅当此发送器已启动m2m_changed信号时才调用该函数.
    有另一种注册接收器功能的方法；它包括使用Signal对象的connect()方法.
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    instance.total_likes = instance.users_like.count()
    instance.save()

