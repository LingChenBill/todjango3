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
