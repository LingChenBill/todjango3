####1.创建自己应用tag - simple_tag.
```bash
register = template.Library()

@register.simple_tag
def total_posts():

在template中的html中加载这个自定义的tag(simple_tag)
{% load blog_tags %}
{% total_posts %} 
```

####2.定制自己排版的tag.
```bash
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

tag的显示内容:latest_posts.html:
<ul>
  {% for post in latest_posts %}
    <li>
      <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>

使用:
{% show_latest_posts %}
```

####3.使用models中的聚合函数来统计comments总计.
```bash
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

使用:
<h3>Most commented posts</h3>
<!--显示最多评论的posts.-->
{% get_most_commented_posts as most_commented_posts %}
<ul>
  {% for post in most_commented_posts %}
    <li>
      <a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
```

####4.markdown依赖安装.
```bash
pip install markdown

from django.utils.safestring import mark_safe

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

使用:
<!--加载自己定制的tag.-->
{% load blog_tags %}

<!--truncatewords_html过滤器会在一定数量的单词后截断字符串, 避免未关闭的html标记. -->
{{ post.body | markdown | truncatewords_html:30 }}
```

####5.sitemap网站导航设置.
`settings.py`设置:
```text
# sitemap 设置.
SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'taggit',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

生效.
python manage.py migrate
```
`sitemaps.py`:
```python
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
```
`urls.py`:
```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    # 配置网站导航.
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]
```
`访问sitemap`:
```text
http://127.0.0.1:8000/sitemap.xml
```
`可以设置domain域名`:
```text
http://127.0.0.1:8000/admin/sites/site/

将域名改为:
localhost:8000
```
#### 6.feed设置.
创建`feeds.py` :
```python
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
```
配置urls:
```bash
path('feed/', LatestPostsFeed(), name='post_feed'),
```
访问url:
```bash
http://localhost:8000/blog/feed/
```
setting.py:
```text
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myblog',
        'USER': 'myblog',
        'PASSWORD': 'myblog'
    }
```
install postgresql psycopg2:
```bash
pip install psycopg2-binary
```
db migrate:
```bash
python manage.py migrate
python manage.py createsuperuser
admin@admin.com
admin
admin

python manage.py runserver

http://localhost:8000/admin/
admin
admin
```
