####1.创建工程
```bash
django-admin startproject myshop

django-admin startapp shop
```
`settings.py`:
```python
'shop.apps.ShopConfig',
```
####2.创建models.
`models.py`中, 创建`Category`和`Product`模型. 图片处理, 安装依赖:
```bash
pip install Pillow
```
数据迁移:
```bash
python manage.py makemigrations

python manage.py migrate
```

