#### 1.配置email.
```bash
# 将email发送到console中, 便于test.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### 2. 测试发送email.
```bash
python manage.py shell

>>> from django.core.mail import send_mail
>>> send_mail('Django mail', 'This e-mail was sent with Django.', 'your_ account@gmail.com', ['your_account@gmail.com'], fail_silently=False)

Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Django mail
From: your_ account@gmail.com
To: your_account@gmail.com
Date: Sun, 27 Mar 2022 10:21:30 -0000
Message-ID: <164837649014.3404.3967982503542974045@1.0.0.127.in-addr.arpa>

This e-mail was sent with Django.
-------------------------------------------------------------------------------
1
```

#### 3.执行model的数据迁移.
```bash
python manage.py makemigrations blog

python manage.py migrate
```

#### 4.安装tag的依赖.
```bash
pip install django_taggit

# 添加标签管理器.
tags = TaggableManager()

python manage.py makemigrations blog
python manage.py migrate
```

#### 5.tag标签shell使用.
```bash
python manage.py shell

>>> from blog.models import Post
>>> post = Post.objects.get(id=2)
>>> post
<Post: There's the django.>

# 添加标签.
>>> post.tags.add('music', 'jazz', 'django')
>>> post.tags.all()
<QuerySet [<Tag: jazz>, <Tag: django>, <Tag: music>]>

# 删除标签.
>>> post.tags.remove('music')
>>> post.tags.all()
<QuerySet [<Tag: jazz>, <Tag: django>]>
```

#### 6.标签的管理页面.
```text
python manage.py runserver

# 标签管理页面.
http://127.0.0.1:8000/admin/taggit/tag/

# 可以在post的编辑页面, 设置每个post的标签.
http://127.0.0.1:8000/admin/blog/post/
```
