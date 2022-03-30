#! /usr/bin/python3
# -*- coding:utf-8 -*-
# @Time: 2022/3/30
# @Author: Lingchen
# @Prescription:
from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """
    构建网站post导航.
    """
    # changefreq和priority属性表示帖子页面的更改频率及其在网站中的相关性.
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        """
        返回要包含在此网站地图中的对象的查询集.
        :return:
        """
        return Post.published.all()

    def lastmod(self, obj):
        """
        lastmod方法接收items()返回的每个对象，并返回上次修改的对象.
        :param obj:
        :return:
        """
        return obj.updated
