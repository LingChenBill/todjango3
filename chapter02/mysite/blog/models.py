from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.


class PublishedManager(models.Manager):
    """
    创建Model管理器.
    """
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
                          .filter(status='published')


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

    objects = models.Manager()
    published = PublishedManager()
    # 标签管理. 标签管理器将允许您添加、检索和删除Post对象中的标签.
    tags = TaggableManager()

    class Meta:
        """
        按publish字段按默认降序对结果进行排序.
        """
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        获取详细post的url路径.
        :return:
        """
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    """
    评价类.
    """
    # comment vs post: many to one的关系.
    # related_name='comments': 检索的关联名称. 1) comment.post. 2) post.comments.all()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # active布尔字段，您将使用该字段手动停用不适当的评论.
    active = models.BooleanField(default=True)

    class Meta:
        # 默认情况下，可以使用创建的字段按时间顺序对注释进行排序.
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


