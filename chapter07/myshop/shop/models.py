from django.db import models

# Create your models here.


class Category(models.Model):
    """
    商品类别model.
    类别模型由名称字段和唯一slug字段组成（唯一表示创建索引）.
    """
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    商品model.
    """
    # 这是一对多关系：一个产品属于一个类别，而一个类别包含多个产品.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    name = models.CharField(max_length=200, db_index=True)
    # 该产品的slug可以构建漂亮的URL.
    slug = models.CharField(max_length=200, db_index=True)
    # 商品图片(可选项).
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    # 产品的可选描述.
    description = models.TextField(blank=True)

    # 该字段使用Python的十进制. 十进制类型来存储一个固定的精确的十进制数.
    # 使用"最大位数"属性和"小数位数"属性设置最大位数(包括小数位数).
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # 指示产品是否可用的布尔值或者不是, 它将用于启用/禁用目录中的产品.
    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        # 使用index_together元选项为id和slug FIELD一起指定索引.
        # 定义这个索引是因为计划同时按id和slug查询产品. 这两个field都被索引在一起，以提高使用这两个field的查询的性能.
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
