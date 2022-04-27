####1.创建折扣app.
```bash
python manage.py startapp coupons
```
将app添加到主工程中, `chapter09/myshop/myshop/settings.py`
```python
'coupons.apps.CouponsConfig',
```
创建折扣model, `chapter09/myshop/coupons/models.py`:
```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Coupon(models.Model):
    """
    折扣model.
    """
    # 用户必须输入的代码，以便将优惠券应用于他们的帐户购买.
    code = models.CharField(max_length=50, unique=True)
    # 指示优惠券何时到期的日期时间值有效的.
    valid_from = models.DateTimeField()
    # 指示优惠券何时到期的日期时间值无效的.
    valid_to = models.DateTimeField()

    # 要应用的折扣率（这是一个百分比，因此它需要值, 从0到100). 使用此字段的验证器来限制最小值和最大可接受值.
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    # 指示优惠券是否处于活动状态的布尔值.
    active = models.BooleanField()

    def __str__(self):
        return self.code
```
数据迁移入DB:
```bash
python manage.py makemigrations

python manage.py migrate
```
修改文件:
```text
chapter09/myshop/myshop/urls.py
chapter09/myshop/cart/views.py
chapter09/myshop/cart/cart.py
chapter09/myshop/coupons/admin.py
chapter09/myshop/coupons/apps.py
chapter09/myshop/coupons/forms.py
chapter09/myshop/coupons/models.py
chapter09/myshop/coupons/tests.py
chapter09/myshop/coupons/urls.py
chapter09/myshop/coupons/views.py
```
修改templates:
```text
chapter09/myshop/orders/templates/orders/order/create.html
chapter09/myshop/cart/templates/cart/detail.html
```
####2.app国际化.
settings.py配置, `chapter09/myshop/myshop/settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# languages.
# "语言"设置包含两个元组，由语言代码和名称组成.
LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
)

# 语言包路径.
# 最先出现的区域设置路径具有最高优先级.
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en'
```
标准翻译:
```python
from django.utils.translation import gettext as _
output = _('Text to translated.')
output
Out[4]: 'Text to translated.'
output_1 = _('欢迎来到这里.') 
output_1
Out[6]: '欢迎来到这里.'
month = _('April')
day = '14'
output = _('Today is %(month)s %(day)s') % {'month': month, 'day': day}
output
Out[10]: 'Today is April 14'
```
设置翻译, `chapter09/myshop/myshop/settings.py`:
```python
from django.utils.translation import gettext_lazy as _

# "语言"设置包含两个元组，由语言代码和名称组成.
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)
```
生成翻译文件:
```bash
% django-admin makemessages --all
processing locale es
processing locale en
```
修改文件,`chapter09/myshop/locale/es/LC_MESSAGES/django.po`:
```text
#: myshop/settings.py:132
msgid "English"
msgstr "Inglés"

#: myshop/settings.py:133
msgid "Spanish"
msgstr "Español"
```
编译:
```bash
django-admin compilemessages
```
修改model, `chapter09/myshop/orders/models.py`:
```python
from django.utils.translation import gettext_lazy as _

first_name = models.CharField(_('first_name'), max_length=50)
last_name = models.CharField(_('last_name'), max_length=50)
email = models.EmailField(_('e-mail'))
address = models.CharField(_('address'), max_length=250)
postal_code = models.CharField(_('postal_code'), max_length=20)
city = models.CharField(_('city'), max_length=100)
```
修改templates, `chapter09/myshop/shop/templates/shop/base.html`:
```html
{% load i18n %}

{% block title %}{% trans 'My shop' %}{% endblock %}</title>

{% blocktrans with total=cart.get_total_price count items=total_items %}
  {{ items }} item, ¥{{ total }}
{% plural %}
  {{ items }} item, ¥{{ total }}
{% endblocktrans %}
```
