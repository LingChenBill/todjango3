#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/3/29
# @Author: Lingchen
# @Prescription:
# blog应用自己的tag标签.
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from ..models import Post
import markdown

# 注册自己的tag和filter.
register = template.Library()


@register.simple_tag
def total_posts():
    """
    返回状态是publish的posts总计.
    :return:
    """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
    定制显示最新的默认是5个posts.
    只在自己的html中使用.
    :param count:
    :return:
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """
    显示最多评论的posts.
    annotate: 汇总每个帖子的评论总数.
    在每个帖子对象的total_comments中存储注释数.
    :param count:
    :return:
    """
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """
    markdown过滤器.
    将函数命名为markdown_format，并将filter标记命名为模板中使用的markdown，例如{variable | markdown}.
    Django逃避过滤器生成的HTML代码；HTML实体的字符将替换为其HTML编码的字符。例如，<p>被转换为&lt;p&gt;.
    由Django提供的mark_safe函数，用于将结果标记为要在模板中呈现的安全HTML.
    :param text:
    :return:
    """
    return mark_safe(markdown.markdown(text))
