#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/3/31
# @Author: Lingchen
# @Prescription:
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    """
    Django有一个内置的syndication feed框架，
    可以使用该框架动态生成RSS或Atom feed，其方式与使用网站框架创建网站地图类似.
    title、link和description属性对应于<title>、<link>和<description>RSS元素.
    """
    title = 'My blog'
    # reverse_lazy（）实用程序函数是reverse（）的一个延迟计算版本. 它允许您在加载项目的URL配置之前使用URL反转.
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self):
        """
        仅检索此订阅源最近发布的5个帖子.
        :return:
        """
        return Post.published.all()[:5]

    def item_title(self, item):
        """
        item_title（）和item_description（）方法将接收items（）返回的每个对象，并返回每个项目的标题和说明.
        :param item:
        :return:
        """
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
