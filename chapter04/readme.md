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
