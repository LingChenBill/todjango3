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
####4.图片详情.
`models.py`:
```python
def get_absolute_url(self):
    """
    图片地址.
    :return:
    """
    return reverse('images:detail', args=[self.id, self.slug])
```
`views.py`:
```python
def image_detail(request, id, slug):
    """
    图片详细信息.
    :param request:
    :param id:
    :param slug:
    :return:
    """
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image})
```
`urls.py`:
```python
# 图片详细信息.
path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
```
`detail.html`:
```html
{% extends "base.html" %}

{% block title %}{{ image.title }}{% endblock %}

{% block content %}
  <h1>{{ image.title }}</h1>

  <img src="{{ image.image.url }}" class="image-detail">

  {% with total_likes=image.users_like.count %}
    <div class="image-info">
      <div>
        <span class="count">
          {{ total_likes }} like{{ total_likes | pluralize }}
        </span>
      </div>
      {{ image.description | linebreaks }}
    </div>
    <div class="image-likes">
      {% for user in image.users_likes.all %}
        <div>
          <img src="{{ user.profile.photo.url }}">
          <p>{{ user.first_name }}</p>
        </div>
      {% empty %}
        Nobody likes this image yet.
      {% endfor %}
    </div>
  {% endwith %}
{% endblock %}
```
```text
访问图片网址:
https://localhost:8000/media/images/2022/04/05/andrew-ling-IopOGhYjpfU.jpg
将点击图片收藏标签, 将该图片加入到图片like中. 可以跳转到图片详情中.
```
####5.图片缩略图.
安装依赖:
```bash
pip install easy-thumbnails
```
将应用加入已安装app列表:
```python
'easy_thumbnails',
```
数据迁移, 生成对应的表结构:
```bash
python manage.py migrate
```
thumbnail的官网:
```text
https://easy-thumbnails.readthedocs.io/
```
网页加载图片:
```html
<!--加载缩略图库.-->
{% load thumbnail %}

<!--通过使用值0，定义一个固定宽度为300像素、高度灵活的缩略图，以保持纵横比.-->
<a href="{{ image.image.url }}">
  <!--<img src="{% thumbnail image.image 300x0 %}" class="image-detail">-->
  <!--<img src="{% thumbnail image.image 300x0 quality=100 %}" class="image-detail">-->
  <img src="{% thumbnail image.image 300x200 quality=50 %}" class="image-detail">
</a>
```
####6.图片的ajax喜欢操作.
`base.html`:
```html
<script src="{% static 'js/jquery.min.js' %}"></script>
<!--JS Cookie是一个用于处理Cookie的轻量级JavaScript API.-->
<script src="{% static 'js/js.cookie.min.js' %}"></script>
<script>
// 获取csrf_token.
var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // 这些HTTP方法不需要CSRF保护.
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// 您可以使用$.ajaxSetup来处理jQuery AJAX请求.
// 如果执行请求，则检查请求方法是否安全，以及当前请求是否跨域.
// 如果请求不安全，则使用从cookie获得的值设置X-CSRFToken头.
// 此设置将应用于使用jQuery执行的所有AJAX请求.
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossOrigin) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});

$(document).ready(function(){
  {% block domready %}
  {% endblock %}
});
</script>
```
`view.py`:
```python
@ajax_required
@login_required
@require_POST
def image_like(request):
    """
    图片喜爱/不喜爱操作.
    需要登录的装饰器阻止未登录的用户访问此视图.
    如果HTTP请求没有通过POST完成，require_POST decorator将返回一个HttpResponseNotAllowed对象（状态代码405）.
    这样，您只允许对该视图进行POST请求。
    :param request:
    :return:
    """
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})

        except:
            pass

    return JsonResponse({'status': 'error'})
```
`urls.py`:
```python
# 图片喜欢操作.
path('like/', views.image_like, name='like'),
```
`detail.html`:
```html
<!--ajax操作.-->
{% block domready %}
  $('a.like').click(function(e) {
    e.preventDefault();

    $.post('{% url "images:like" %}',
           {
              id: $(this).data('id'),
              action: $(this).data('action')
           },
           function(data) {
              if (data['status']) {
                var previous_action = $('a.like').data('action');

                // 替换data, action.
                $('a.like').data('action', previous_action == 'like'? 'unlike' : 'like');
                // 替换按钮文本内容.
                $('a.like').text(previous_action == 'like'? 'Unlike' : 'Like');

                var previous_likes = parseInt($('span.count .total').text());
                // 更新like的数据.
                $('span.count .total').text(previous_action == 'like'? previous_likes + 1 : previous_likes - 1);
              }
           }
    );
  });
{% endblock %}
```
装饰器配置:
```python
from django.http import HttpResponseBadRequest


def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__=f.__name__
    return wrap
```
网址验证.
```bash
https://localhost:8000/media/images/2022/04/05/world.jpg
```
####7.图片列表ajax请求.
`view.py`:
```python
@login_required
def image_list(request):
    """
    图片列表.
    :param request:
    :return:
    """
    images = Image.objects.all()
    # 构建Paginator对象对结果进行分页，每页检索八幅图像.
    paginator = Paginator(images, 8)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # 若请求是一个ajax, 且页码超过界限, 返回一个空的对象.
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    if request.is_ajax():
        # 这个模板将只包含请求页面的图像.
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images',
                       'images': images})

    # 这个模板将扩展base.html模板来显示整个页面，并将包括list_ajax.html模板, 用来包括图像列表.
    return render(request,
                  'images/image/list.html',
                  {'section': 'images',
                   'images': images})
```
`urls.py`:
```python
# 图片列表.
path('', views.image_list, name='list'),
```
templates:
`list.html`:
```html
{% extends "base.html" %}

{% block title %}Images bookmarked{% endblock %}

{% block content %}
  <h1>Images bookmarked</h1>

  <div id="image-list">
    <!--包含图片列表画面.-->
    {% include "images/image/list_ajax.html" %}
  </div>
{% endblock %}

{% block domready %}
  <!--当前的页码.-->
  var page = 1;
  <!--判断当前页码是否最后一页, 是否到了图片数的界限.-->
  var empty_page = false;
  <!--判断是否发送ajax请求.-->
  var block_request = false;

  <!--使用$(window).scroll()以捕获滚动事件和定义一个处理函数.-->
  $(window).scroll(function(){
    var margin = $(document).height() - $(window).height() - 200;
    if ($(window).scrollTop() > margin && empty_page == false && block_request == false) {
      block_request = true;
      page += 1;

      $.get('?page=' + page, function(data) {
        if (data == '') {
          empty_page = true;
        }
        else {
          block_request = false;
          $('#image-list').append(data);
        }
      });
    }
  });
{% endblock %}
```
`list_ajax.html`:
```html
<!--加载缩略图.-->
{% load thumbnail %}

{% for image in images %}
  <div class="image">
    <a href="{{ image.get_absolute_url }}">
      <!--你在图像上迭代并为每个图像生成一个方形缩略图.将缩略图的大小规格化为300x300像素.-->
      <!--还可以使用智能裁剪选项, 此选项表示必须通过从熵最小的边缘移除切片，将图像增量裁剪到所需大小.-->
      {% thumbnail image.image 300x300 crop="smart" as im %}

      <a href="{{ image.get_absolute_url }}">
        <img src="{{ im.url }}">
      </a>
    </a>
    <div class="info">
      <a href="{{ image.get_absolute_url }}" class="title">
        {{ image.title }}
      </a>
    </div>
  </div>
{% endfor %}
```
访问网址, 验证图片列表:
```bash
https://localhost:8000/images
```

