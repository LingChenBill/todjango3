####1.创建工程和app.
```bash
django-admin startproject bookmarks

cd bookmarks

django-admin startapp account
```
配置app, `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.accountConfig',
]
```
数据迁移:
```bash
python manage.py migrate
```
####2.创建用户
用户form, `forms.py`:
```python
from django import forms


class LoginForm(forms.Form):
    """
    用户登录form.
    """
    username = forms.CharField()
    # input -> password type.
    password = forms.CharField(widget=forms.PasswordInput)
```
用户view, `views.py`:
```python
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.


def user_login(request):
    """
    用户登录view操作.
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 用户form实例化.
        form = LoginForm(request.POST)
        # 验证用户form.
        if form.is_valid():
            # 解析用户数据.
            cd = form.cleaned_data
            # 与DB用户数据验证.
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    # 若用户是激活的, 使用login方法将用户信息存入session.
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        # 初期化user form给用户登录画面.
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
```
配置url, `urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    # login.
    path('login/', views.user_login, name='login'),
]
```
注册到bookmarks的urls:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 注入account urls.
    path('account/', include('account.urls')),
]
```
配置templates, `login.html`:
```html
{% extends "base.html" %}

{% block title %}Log-in{% endblock %}

{% block content %}
  <h1>Log-in</h1>
  <p>Please, use the following for to log-in:</p>

  <form method="post">
    {{ form.as_p }}

    {% csrf_token %}

    <p>
      <input type="submit" value="Log in" />
    </p>
  </form>
{% endblock %}
```
配置base.html和基础css. 创建超级用户:
```bash
python manage.py createsuperuser

admin
admin
```
启动工程:
```bash
python manage.py runserver
```
访问`http://127.0.0.1:8000/account/login/`, 验证用户.
####3.class-based views.
`views.py`:
```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """
    用户登录dashboard.
    login_required decorator检查当前用户是否经过身份验证.
    如果用户经过身份验证，则执行装饰视图;
    如果用户未通过身份验证，它会将用户重定向到登录URL，并将最初请求的URL作为名为next的GET参数.
    :param request:
    :return:
    """
    # 还可以定义一个section变量. 您将使用此变量跟踪用户正在浏览的站点部分.
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

```
`urls.py`:
```python
# 配置用户登录的dashboard url.
path('', views.dashboard, name='dashboard'),
# auth class-based login views.
path('login/', auth_views.LoginView.as_view(), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
```
template:
```text
base.html
registration/login.html
registration/logout.html
account/dashboard.html
```
`settings.py`:
```python
INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 配置用户登录url.
# 将用户重定向到哪个URL, 如果请求中不存在next参数，则成功登录.
LOGIN_REDIRECT_URL = 'dashboard'
# 重定向用户登录的URL(例如，使用登录名, 需要装饰程序).
LOGIN_URL = 'login'
# 重定向用户登出.
LOGOUT_URL = 'logout'
```
####4.修改用户密码
使用auth的class-based views:
`urls.py`:
```python
# 密码修改urls.
path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
```
templates:
```text
registration/password_change_form.html
registration/password_change_done.html
```
访问站点, 进行用户密码验证.
`http://localhost:8000/account/password_change/`
```text
admin
Aa.com..
Aa.com..
```
####5.重置密码.
使用auth中的class-based views, `views.py`:
```python
# 重置密码urls.
path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
```
创建template, 注意html的名称不要写错.
```text
password_reset_complete.html
password_reset_confirm.html
password_reset_done.html
password_reset_email.html
password_reset_form.html
```
配置email进行验证.
`settings.py`:
```python
# Email配置.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
访问站点, 进行密码重置:
`http://localhost:8000/account`
在输入email时, 要输入用户创建时的email, 否则在控制台中看不到email信息(验证不通过).
####6.用户登录.
form表单设置:
```python
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    """
    用户注册form.
    """
    # 添加表单的项目.
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        # 表单的元素.
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """
        对照第一个密码检查第二个密码，如果密码不匹配，不让表单is_valid()验证通过.
        当您通过调用表单的is_valid（）方法验证表单时，将完成此检查.
        :return:
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match. ')
        return cd['password2']
```
`views.py`:
```python
from .forms import LoginForm, UserRegistrationForm

def register(request):
    """
    用户注册.
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # 保存用户输入的原始密码时，可以使用处理哈希的用户模型的set_password()方法.
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'user_form': user_form})

```
url配置,`urls.py`:
```python
# 用户注册.
path('register/', views.register, name='register'),
```
templates:
```text
register.html
register_done.html
```
访问站点, 进行用户注册验证:
`http://127.0.0.1:8000/account/register/`
```text
lingchen
Aa.com..
```
####7.用户增强.
model中用户增加配置:
```python
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
```
图片处理, 安装依赖:
```bash
pip install Pillow
```
数据迁移:
```bash
python manage.py makemigrations

python manage.py migrate
```
注册profile到admin管理中:
```python
from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    profile配置.
    """
    list_display = ['user', 'date_of_birth', 'photo']
```
启动服务, 查看profile:
```bash
python manage.py runserver
```
`http://127.0.0.1:8000/admin`, 可以添加profile.
用户编辑profile, `forms.py`:
```python
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    """
    用户登录form.
    """
    username = forms.CharField()
    # input -> password type.
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """
    用户注册form.
    """
    # 添加表单的项目.
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        # 表单的元素.
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """
        对照第一个密码检查第二个密码，如果密码不匹配，不让表单is_valid()验证通过.
        当您通过调用表单的is_valid（）方法验证表单时，将完成此检查.
        :return:
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match. ')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """
    用户编辑form.
    这将允许用户编辑他们的名字，姓氏，和电子邮件，这是内置Django用户模型的属性.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """
    用户profile编辑form.
    允许用户编辑您需要的配置文件数据保存在自定义配置文件模型中.
    用户可以编辑他们的注册日期出生并上传他们个人资料的图片.
    """
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
```
`views.py`:
```python
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

# 注册用户中, 添加profile的创建.
# 用户配置信息.
Profile.objects.create(user=new_user)

@login_required
def edit(request):
    """
    用户编辑view设置.
    UserEditForm用于存储内置用户模型的数据，ProfileEditForm用于在自定义配置文件模型中存储附加的profile数据.
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
```
配置`urls.py`:
```python
# 用户profile编辑.
path('edit/', views.edit, name='edit'),
```
添加templates:
```text
edit.html
```
在`dashboard.html`中添加相关链接.
```html
Welcome to your dashboard.
You can <a href="{% url 'edit' %}">edit your profile</a>
or <a href="{% url 'password_change' %}">change your password</a>.
```
####8.message设置.
使用`django.contrib. messages.context_processors.messages`, 在templates中可以直接使用messages变量.
```python
from django.contrib import messages

# 信息设置.
messages.success(request, 'Profile updated successfully.')
```
template中, `base.html`:
```html
<!--message设置.-->
<!--消息框架包括上下文处理器django.contrib. messages.context_processors.messages，-->
<!--它将messages变量添加到请求上下文中. 可以在项目TEMPLATES设置的上下文列表中找到它.-->
<!--可以使用模板中的messages变量向用户显示所有现有消息.-->
{% if messages %}
<ul class="messages">
  {% for message in messages %}
    <li class="{{ message.tags }}">
      {{ message | safe }}
      <a href="#" class="close">x</a>
    </li>
  {% endfor %}
</ul>
{% endif %}
```
####9.定制认证后台.
定制`authentication.py`:
```python
from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    自定义认证后台.
    一个简单的身份验证后端.
    authenticate()方法接收请求对象以及用户名和密码可选参数.
    您可以使用不同的参数，但您可以使用用户名和密码使后端立即与身份验证框架视图一起工作.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            # 检索具有给定电子邮件地址的用户.
            user = User.objects.get(email=username)
            # 并使用用户模型的内置check_password（）方法检查密码.
            # 此方法处理密码散列，以将给定密码与存储在数据库中的密码进行比较.
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```
`settings.py`配置:
```python
# 定制认证后台.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
]
```
####10.社交认证.
安装依赖:
```bash
pip install social-auth-app-django
```
`settings.py`配置:
```python
# 配置可信任的域名.
ALLOWED_HOSTS = ['mybookmarks.com', 'localhost', '127.0.0.1']

# 定制认证后台.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
]
```
数据迁移:
```bash
python manage.py migrate
```
安装https相关依赖:
```bash
pip install django-extensions

# 访问https:mysite.com:8000/account没有成功.
# pip install werkzeug
# pip install django-werkzeug-debugger-runserver

pip install pyOpenSSL

# 生成认证文件:
openssl req -new -x509 -newkey rsa:4096 -keyout server.key -out server.crt

python manage.py runserver_plus --cert-file cert.crt
python manage.py runserver_plus --cert server.crt mysite.com:8000
```
