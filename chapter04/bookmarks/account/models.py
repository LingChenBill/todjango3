from django.db import models
from django.conf import settings

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
