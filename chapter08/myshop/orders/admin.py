from django.contrib import admin
from django.http import HttpResponse
from .models import Order, OrderItem
import csv
import datetime

# Register your models here.


class OrderItemInline(admin.TabularInline):
    """
    使用OrderItem模型的ModelInline类将其作为内联包含在OrderAdmin类中.
    内联允许您在与其相关模型相同的编辑页面上包含模型.
    """
    model = OrderItem
    # 关联的商品ID.
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    """
    csv导出.
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    # 创建一个HttpResponse实例，指定text/csv内容
    # 浏览器响应必须被视为CSV文件. 可以添加一个内容处置头，以指示HTTP响应包含附加的file.
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    # 创建将写入响应对象的CSV编写器对象.
    writer = csv.writer(response)

    # 可以使用get_fields()方法动态获取模型field模型的meta选项. 排除多对多和一对多关系.
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # 标题行.
    writer.writerow([field.verbose_name for field in fields])

    # 迭代给定的查询集，并为返回的每个对象写一行在QuerySet.
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            # 因为CSV的输出值必须是字符串，所以需要设置datetime对象的格式.
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')

            data_row.append(value)
        writer.writerow(data_row)

    return response
# 在"操作"下拉列表中自定义操作的显示名称通过在函数上设置short_description属性来创建管理站点的元素.
export_to_csv.short_description = 'Export to CSV'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code',
                    'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']

    # 关联的商品订单item.
    inlines = [OrderItemInline]

    # 将export_to_csv管理操作添加到OrderAdmin类.
    actions = [export_to_csv]

