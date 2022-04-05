from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


class Image(models.Model):
    """
    图片模型.
    """
    # 这表示为该图像添加书签的用户对象.
    # 这是外键字段，因为它指定了一对多关系：用户可以发布多个图像，但每个图像都由一个用户发布.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    # 只包含字母、数字、下划线或数字的短标签连字符用于构建漂亮友好的URL.
    slug = models.SlugField(max_length=200, blank=True)

    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    # 使用db_index=True使Django在数据库中为此字段创建索引.
    created = models.DateField(auto_now_add=True, db_index=True)

    # Django在ManyToManyField中使用两个模型的主键创建一个中间连接表.
    # ManyToManyField可以在两个相关模型中任意一个中定义.
    # ManyToManyField的related_name属性允许您将相关对象的关系命名回这个对象.
    # ManyToManyFields提供了一个多对多管理器，允许您检索相关对象，
    # 例如image.users_like.all(), 或从用户对象（如user）获取它们, 使用user.images_liked.all().
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_likes',
                                        blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        重写图像模型的save()方法，根据标题字段的值自动生成slug字段.
        导入slugify()函数，并向图像模型添加save()方法.
        :param args:
        :param kwargs:
        :return:
        """
        if not self.slug:
            # 当slug为空时, 根据title来自动生成slug.
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
