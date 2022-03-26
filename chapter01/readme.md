#### 1.创建工程.
```bash
django-admin startproject mysite
```

#### 2.数据应用.
```bash
python manage.py migrate
```

#### 3.启动应用.
```bash
python manage.py runserver
```

#### 4.创建app.
```bash
python manage.py startapp blog
```

#### 5.数据迁移.
```bash
python manage.py makemigrations blog
```

#### 6.查看生成的sql.
```bash
python manage.py sqlmigrate blog 0001
```

#### 7.创建超级用户.
```bash
python manage.py createsuperuser
admin
admin
```

#### 8.query api
```bash
python manage.py shell

>>> from django.contrib.auth.models import User
>>> from blog.models import Post
>>> user = User.objects.get(username='admin')
>>> post = Post(title='Another post', slug='another post', body='Post body.', author=user)
>>> post.save()

# 创建post.
>>> Post.objects.create(title='One more post', slug='one more post', body='One post body.', author=user)

# 更新post.
>>> post.title = 'New title'
>>> post.save()

# 查询post.
>>> all_posts = Post.objects.all()
>>> all_posts

# 过滤posts.
>>> Post.objects.filter(publish__year=2022)
# 多个过滤条件.
>>> Post.objects.filter(publish__year=2022, author__username='admin')
# 过滤链.
>>> Post.objects.filter(publish__year=2022) \
                .filter(author__username='admin')
# 过滤中排除.
>>> Post.objects.filter(publish__year=2022) \
                .exclude(title__startswith='Why')
# 排序.
>>> Post.objects.order_by('title')
# 降序.
>>> Post.objects.order_by('-title')
# 删除.
>>> post = Post.objects.get(id=1)
>>> post
>>> post.delete()

```

