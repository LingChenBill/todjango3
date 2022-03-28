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