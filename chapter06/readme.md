####1.运行
```bash
python manage.py runserver_plus --cert-file cert.crt

https://localhost:8000/account
```
####2.创建many-2-many模型.
`models.py`:
```python
from django.contrib.auth import get_user_model

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
```
数据迁移:
```bash
python manage.py makemigrations account

python manage.py migrate account
```
####3.创建用户列表和详细信息.
`views.py`:
```python
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User


@login_required
def user_list(request):
    """
    获取用户列表.
    :param request:
    :return:
    """
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    """
    用户详细信息.
    :param request:
    :param username:
    :return:
    """
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)

    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})
```
在`settings.py`中配置, 用户的详细信息url:
```python
from django.urls import reverse_lazy

# 使用user_detail URL模式为用户生成规范的URL.
# 您已经在模型中设计了一个get_absolute_url（）方法，用于返回每个对象的规范url.
# 为模型指定URL的另一种方法是将ABSOLUTE_URL_OVERRIDES设置添加到项目中.
# Django向出现在ABSOLUTE_URL_OVERRIDES设置中的任何模型动态添加get_absolute_url()方法.
# 此方法返回设置中指定的给定模型的相应URL. 返回给定用户的用户详细信息URL.
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}
```
在`python shell`中验证用户url:
```bash
python manage.py shell

from django.contrib.auth.models import User

user = User.objects.latest('id')
str(user.get_absolute_url())
```
####4.创建用户列表和详细信息页面.
```text
detail.html
list.html
```
`urls.py`:
```python
# 用户列表.
path('users/', views.user_list, name='user_list'),
# 用户详细.
path('users/<username>/', views.user_detail, name='user_detail'),
```
在`base.html`中修改导航people的链接:
```html
<li {% if section == "people" %}class="selected"{% endif %}>
  <a href="{% url 'user_list' %}">People</a>
</li>
```
访问网页进行验证:
```text
https://localhost:8000/account/users/
```
####5.用户follow操作.
`views.py`:
```python
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import Profile, Contact
from common.decorators import ajax_required

@ajax_required
@require_POST
@login_required
def user_follow(request):
    """
    用户follow操作. POST提交数据.
    :param request:
    :return:
    """
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})
```
`urls.py`:
```python
# 用户follow.
path('users/follow', views.user_follow, name='user_follow'),
```
template的`detail.html`:
```html
{% block domready %}
  $('a.follow').click(function(e) {
    e.preventDefault();

    $.post('{% url "user_follow" %}',
      {
        id: $(this).data('id'),
        action: $(this).data('action')
      },
      function(data) {
        if (data['status'] == 'ok') {
          var previous_action = $('a.follow').data('action');
          <!-- 切换data的action.-->
          $('a.follow').data('action', previous_action == 'follow'? 'unfollow' : 'follow');
          <!--切换链接文本.-->
          $('a.follow').text(previous_action == 'follow'? 'Unfollow' : 'Follow');
          <!--更新总的follow数.-->
          var previous_followers = parseInt($('span.count .total').text());
          $('span.count .total').text(previous_action == 'follow'? previous_followers + 1 : previous_followers - 1);
        }
      }
    );
  });
{% endblock %}
```
访问网页, 进行验证.
####6.创建actions的app应用.
```bash
python manage.py startapp actions
```
`settings.py`中配置apps:
```python
'actions.apps.ActionsConfig',
```
创建actions的model,`models.py`:
```python
from django.db import models

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
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
```
####7.ContentTypes的框架.
```python
'django.contrib.contenttypes',
```
在shell中验证:
```bash
python manage.py shell

from django.contrib.contenttypes.models import ContentType
image_type = ContentType.objects.get(app_label='images', model='image')

image_type
<ContentType: images | image>

image_type.model_class()
images.models.Image

from images.models import Image
ContentType.objects.get_for_model(Image)
<ContentType: images | image>
```
在model中补充contenttypes内容, `models.py`:
```python
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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
```
数据迁移:
```bash
python manage.py makemigrations actions

python manage.py migrate actions
```
将action注册到admin中,`admin.py`:
```python
from django.contrib import admin
from .models import Action

# Register your models here.


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    """
    将Action注册到admin管理中.
    """
    list_display = ('user', 'verb', 'target', 'created')
    list_filter = ('created',)
    search_fields = ('verb',)
```
在网页端验证:
```bash
python manage.py runserver_plus --cert-file cert.crt

https://localhost:8000/admin/actions/action/add/
```
创建action的utils方法:
```python
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    """
    创建action.
    允许您创建可选包含目标对象的操作.
    您可以在代码中的任何位置使用此函数作为向活动流添加新操作的快捷方式.
    :param user:
    :param verb:
    :param target:
    :return:
    """
    action = Action(user=user, verb=verb, target=target)
    action.save()
```
####8.创建用户操作.
在各个create view中的creat操作后, 添加create_action操作.
```python
views.py

# 储存用户like操作.
create_action(request.user, 'likes', image)

# 储存图片创建操作.
create_action(request.user, 'bookmarked image', new_item)

# 储存用户follow操作行为.
create_action(request.user, 'is following', user)

from actions.models import Action

@login_required
def dashboard(request):
    """
    用户登录dashboard.
    login_required decorator检查当前用户是否经过身份验证.
    如果用户经过身份验证，则执行装饰视图;
    如果用户未通过身份验证，它会将用户重定向到登录URL，并将最初请求的URL作为名为next的GET参数.
    添加用户操作actions.
    :param request:
    :return:
    """
    # 从数据库中检索所有操作，当前用户执行的操作除外.
    actions = Action.objects.exclude(user=request.user)
    # 如果用户正在跟踪其他用户，则可以将查询限制为仅检索他们跟踪的用户执行的操作.
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    # 限制10个查询结果.
    actions = actions[:10]

    # 还可以定义一个section变量. 您将使用此变量跟踪用户正在浏览的站点部分.
    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'actions': actions})
```
`utils.py`:
```python
import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    """
    创建action.
    允许您创建可选包含目标对象的操作.
    您可以在代码中的任何位置使用此函数作为向活动流添加新操作的快捷方式.
    避免保存重复的操作，并返回布尔值来告诉您是否保存了该操作.
    :param user:
    :param verb:
    :param target:
    :return:
    """
    now = timezone.now()

    # 使用last_minute变量存储一分钟后的日期时间并检索用户此后执行的任何相同操作.
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
```
在`account/views.py`中的`dashboard`方法中添加actions操作:
```python
@login_required
def dashboard(request):
    """
    用户登录dashboard.
    login_required decorator检查当前用户是否经过身份验证.
    如果用户经过身份验证，则执行装饰视图;
    如果用户未通过身份验证，它会将用户重定向到登录URL，并将最初请求的URL作为名为next的GET参数.
    添加用户操作actions.
    :param request:
    :return:
    """
    # 从数据库中检索所有操作，当前用户执行的操作除外.
    actions = Action.objects.exclude(user=request.user)
    # 如果用户正在跟踪其他用户，则可以将查询限制为仅检索他们跟踪的用户执行的操作.
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    # 限制10个查询结果.
    # actions = actions[:10]

    # select_related方法允许您检索一对多关系的相关对象.
    # 该方法适用于ForeignKey和OneToOne FIELD. 它的工作原理是执行SQL联接，并在SELECT语句中包含相关对象的field.
    # actions = actions.select_related('user', 'user__profile')[:10]

    # prefetch_related()方法适用于多对多和多对一关系, 对每个关系执行单独的查找，并使用Python连接结果.
    # 此方法还支持预取GenericRelation和GenericForeignKey.
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    # 还可以定义一个section变量. 您将使用此变量跟踪用户正在浏览的站点部分.
    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'actions': actions})
```
创建actions的templates,`detail.html`:
```html
{% load thumbnail %}

{% with user=action.user profile=action.user.profile %}
  <div class="action">
    <div class="images">
      {% if profile.photo %}
        {% thumbnail user.profile.photo "80x80" crop="100%" as im %}
        <a href="{{ user.get_absolute_url }}">
          <img src="{{ im.url }}" alt="{{ user.get_full_name }}" class="item-img">
        </a>
      {% endif %}

      {% if action.target %}
        {% with target=action.target %}
          {% if target.image %}
            {% thumbnail target.image "80x80" crop="100%" as im %}
            <a href="{{ target.get_absolute_url }}">
              <img src="{{ im.url }}" class="item-img">
            </a>
          {% endif %}
        {% endwith %}
      {% endif %}
    </div>

    <div class="info">
      <p>
        <span class="date">{{ action.created | timesince }} ago</span>
        <br />
        <a href="{{ user.get_absolute_url }}">
          {{ user.first_name }}
        </a>
        {{ action.verb }}
        {% if action.target %}
          {% with target=action.target %}
            <a href="{{ target.get_absolute_url }}">{{ target }}</a>
          {% endwith %}
        {% endif %}
      </p>
    </div>
  </div>
{% endwith %}
```
在`dashboard.html`中添加actions展示内容.
```html
<h2>What's happening</h2>

<div id="action-list">
{% for action in actions %}
  {% include "actions/action/detail.html" %}
{% endfor %}
</div>
```
访问网址, 以不同用户操作图片, like, follow操作等, 再用一个不同的用户登入, 在dashboard页面中查看actions操作结果.
```html
https://localhost:8000/account/
```
