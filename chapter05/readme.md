####1.图片模型创建,`models.py`:
```python
from django.db import models
from django.conf import settings

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
```
数据迁移:
```bash
python manage.py makemigrations images

python manage.py migrate images
```
在`admin.py`中注册图片`model`:
```python
from django.contrib import admin
from .models import Image

# Register your models here.


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']
```
在`settings.py`中配置`images`app:
```python
INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django_extensions',
    'images.apps.ImagesConfig',
]
```
图片form表单编辑:
```python
from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):
    """
    图片创建form.
    此表单是基于图像模型构建的模型表单，仅包括标题、url和描述.
    用户不会直接在表单中输入图像URL.
    相反，您将为他们提供一个JavaScript工具，用于从外部站点选择图像，您的表单将接收其URL作为参数.
    可以覆盖url字段的默认小部件，以使用HiddenInput小部件.
    """
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

        # 此widgets小部件呈现为带有type=“hidden”属性的HTML输入元素.
        # 你使用这个小部件是因为你不想让用户看到这个字段.
        widgets = {
            'url': forms.HiddenInput,
        }

        def clean_url(self):
            """
            拆分URL以获取file扩展名，并检查它是否为有效的扩展名.
            如果扩展无效，则引发ValidationError并表单实例将不会被验证.
            :return:
            """
            url = self.cleaned_data['url']
            valid_extensions = ['jpg', 'jpeg']
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('The given URL does not match valid image extensions.')
            return url
```
####2.创建图片.
`forms.py`:
```python
class ImageCreateForm(forms.ModelForm):
    """
    图片创建form.
    此表单是基于图像模型构建的模型表单，仅包括标题、url和描述.
    用户不会直接在表单中输入图像URL.
    相反，您将为他们提供一个JavaScript工具，用于从外部站点选择图像，您的表单将接收其URL作为参数.
    可以覆盖url字段的默认小部件，以使用HiddenInput小部件.
    """
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

        # 此widgets小部件呈现为带有type=“hidden”属性的HTML输入元素.
        # 你使用这个小部件是因为你不想让用户看到这个字段.
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        """
        拆分URL以获取file扩展名，并检查它是否为有效的扩展名.
        如果扩展无效，则引发ValidationError并表单实例将不会被验证.
        :return:
        """
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """
        1.通过调用表单的save()方法，可以创建一个新的图像实例使用commit=False.
        2.从表单的数据字典中获取URL.
        3.通过将图像标题slug与原始的file扩展.
        4.使用Python urllib模块下载图像，然后调用方法，将一个ContentFile对象传递给它用下载的ile内容实例化.
          通过这种方式，您可以保存文件转到项目的媒体目录. 传递save=False参数避免将对象保存到数据库.
        5.为了保持与重写的save()方法相同的行为，只有当commit参数为True时，才能将表单保存到数据库中.
        :param force_insert:
        :param force_update:
        :param commit:
        :return:
        """
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # 下载图片.
        response = request.urlopen(image_url)
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)
        if commit:
            image.save()
        return image
```
`urls.py`:
```python
from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    # 图片创建.
    path('create/', views.image_create, name='create'),
]
```
`views.py`:
```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

# Create your views here.


@login_required
def image_create(request):
    """
    图片创建view.
    """
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)

            # 将图片绑定用户.
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully.')

            # 将用户重定向到新图像的规范URL. 你还没有实现了图像模型的get_absolute_url()方法, 你会以后再做.
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})
```
访问图片创建网址:
```text
http://localhost:8000/images/create/?title=world&url=http://localhost:8000/media/images/2022/04/05/world.jpg
```
####3.https访问设置
```text
python manage.py runserver_plus --cert-file cert.crt

将`chapter05/bookmarks/cert.crt`添加到mac的钥匙串中, 将信任关系设置成`始终信任`
用`无痕模式`打开新的chrome浏览器窗口, 
访问站点:

https://127.0.0.1:8000/account/
即可.
```