from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    # CharField -> Varchar
    title = models.CharField(max_length=250)
    # 这是一个用于URL的字段。slug是一个短标签, 只包含字母、数字、下划线或连字符的.
    # 你将使用slug字段可以为你的博客帖子创建漂亮的、对搜索引擎友好的URL.
    # 您已将unique_for_date参数添加到此字段，以便可以使用发布日期和slug为帖子构建URL.
    # django的防止多个帖子在给定日期出现相同的问题.
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # many to one 关系. 一个用户可以写多个Posts. 级联.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # TextField -> Text.
    body = models.TextField()
    # DateTimeField -> Datetime.
    publish = models.DateTimeField(default=timezone.now)
    # auto_now_add 自动创建时间.
    created = models.DateTimeField(auto_now_add=True)
    # auto_now 更新时自动更新时间.
    updated = models.DateTimeField(auto_now=True)
    # 类似类型转换.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        """
        按publish字段按默认降序对结果进行排序.
        """
        ordering = ('-publish',)

    def __str__(self):
        return self.title
