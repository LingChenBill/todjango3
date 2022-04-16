from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    """
    使用OrderItem模型的ModelInline类将其作为内联包含在OrderAdmin类中.
    内联允许您在与其相关模型相同的编辑页面上包含模型.
    """
    model = OrderItem
    # 关联的商品ID.
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                    'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']

    # 关联的商品订单item.
    inlines = [OrderItemInline]
