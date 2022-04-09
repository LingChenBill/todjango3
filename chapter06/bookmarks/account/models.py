from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.


class Profile(models.Model):
    """
    用户model增加配置.
    """
    # 用户一对一字段允许您将profiles与用户关联.
    # 对on_delete参数使用CASCADE，以便在删除用户时也删除其相关的profile.
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=True)
    # 照片是一个图片类型项目. 你需要安装Pillow库来处理图像.
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Contact(models.Model):
    """
    创建一个中介模型来建立用户之间的关系。使用中介模型有两个原因:
    您使用的是Django提供的用户模型，希望避免改变它.
    你想存储建立关系的时间.
    """
    # 创建关系的用户的外键.
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    # 被跟踪用户的外键.
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)

    # 一个日期时间字段，其auto_now_add=True用于存储时间建立关系的时候.
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# 向用户动态添加以下字段.
# 使用Django提供的通用函数get_user_model()检索用户模型.
# 使用Django models的add_to_class()方法对用户模型进行修补.
# 请注意，使用add_to_class()不是向模型中添加Fields的推荐方法.
# 但是，在本例中，您可以利用它来避免创建自定义用户模型，从而保留Django内置用户模型的所有优点.
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))
