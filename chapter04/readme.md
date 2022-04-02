1.创建工程和app.
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
