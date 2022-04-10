from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class Action(models.Model):
    """
    创建action的model, 储存用户活动.
    """
    # 执行操作的用户, 这是Django的外键用户模型.
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)

    # 描述用户执行的操作的动词.
    verb = models.CharField(max_length=255)

    # 指向ContentType模型的ForeignKey字段.
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    # 一个用于存储相关对象.
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    # 基于前两个字段的组合.
    # Django不会在数据库中为GenericForeignKey field创建任何字段.
    # 映射到数据库field的唯一field是target_ct和target_id.
    # 这两个field都有blank=True和null=True属性，因此保存操作对象时不需要目标对象.
    target = GenericForeignKey('target_ct', 'target_id')

    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
