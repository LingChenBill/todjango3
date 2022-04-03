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
