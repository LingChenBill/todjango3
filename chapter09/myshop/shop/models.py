from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.


class Category(TranslatableModel):
    """
    商品类别model.
    类别模型由名称字段和唯一slug字段组成（唯一表示创建索引）.
    django parler通过为每个可翻译模型生成另一个模型来管理翻译.
    """
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True, unique=True)
    )

    class Meta:
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        get_absolute_url()是检索给定对象的url的约定.
        在这里，您使用的是您刚刚在URL中定义的URL模式.
        :return:
        """
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(TranslatableModel):
    """
    商品model.
    django parler生成的ProductTranslation模型包括名称、slug和描述可翻译的field、language代码字段和主产品对象的ForeignKey.
    从产品到产品翻译有一对多的关系. 对于每个产品对象的每种可用语言，都将存在一个ProductTranslation对象.
    """
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        # 该产品的slug可以构建漂亮的URL.
        slug=models.CharField(max_length=200, db_index=True),
        # 产品的可选描述.
        description=models.TextField(blank=True)
    )
    # 这是一对多关系：一个产品属于一个类别，而一个类别包含多个产品.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    # 商品图片(可选项).
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    # 该字段使用Python的十进制. 十进制类型来存储一个固定的精确的十进制数.
    # 使用"最大位数"属性和"小数位数"属性设置最大位数(包括小数位数).
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # 指示产品是否可用的布尔值或者不是, 它将用于启用/禁用目录中的产品.
    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # class Meta:
        # 由于Django使用单独的表进行翻译，因此有一些Django特性是您无法使用的.
        # 无法按翻译字段使用默认排序. 可以在查询中通过已翻译的字段进行筛选，但不能在排序元选项中包含可翻译的字段.
        # ordering = ('name',)
        # 使用index_together元选项为id和slug FIELD一起指定索引.
        # 定义这个索引是因为计划同时按id和slug查询产品. 这两个field都被索引在一起，以提高使用这两个field的查询的性能.
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
