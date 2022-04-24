#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/4/23
# @Author: Lingchen
# @Prescription:
from io import BytesIO
from myshop.celery import app
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
import weasyprint


@app.task
def payment_completed(order_id):
    """
    成功创建订单时发送电子邮件通知的任务.
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)

    subject = f'My Shop - EE Invoice no.{order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'lingchen1316@163.com',
                         [order.email])

    # 生成PDF到BytesIO中.
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    # 加载css.
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # 添加附件.
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # 发送邮件.
    email.send()
