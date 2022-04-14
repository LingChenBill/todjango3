#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/14
# @Author: Lingchen
# @Prescription:
from myshop.celery import app
from django.core.mail import send_mail
from .models import Order


@app.task
def order_created(order_id):
    """
    订单异步任务创建.
    celery任务只是一个用@task修饰的Python函数.任务函数接收订单id参数.
    始终建议在执行任务时仅将ID传递给任务函数和查找对象.
    可以使用Django提供的send_mail()函数向下订单的用户发送电子邮件通知.
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order_id}'

    message = f'Dear {order.first_name}, \n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order_id}.'

    mail_sent = send_mail(subject,
                          message,
                          'lingchen1316@163.com',
                          [order.email])
    return mail_sent
