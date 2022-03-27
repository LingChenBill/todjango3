from django.contrib import admin
from .models import Post

# Register your models here.
# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    “list_display”属性允许您设置要在“ModelAdmin”列表页面上显示的模型.
    @admin.register()替换的register()函数，注册它修饰的ModelAdmin类.
    """
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # 过滤选项.
    list_filter = ('status', 'created', 'publish', 'author')
    # 搜索项.
    search_fields = ('title', 'body')
    # 使用“预填充的_字段”属性，用标题字段的输入预填充slug字段.
    prepopulated_fields = {'slug': ('title', )}
    # 当你有成千上万的用户时，一个查找小部件可以比下拉选择输入扩展得更好.
    raw_id_fields = ('author',)
    # 导航链接，用于在日期层次结构中导航.
    date_hierarchy = 'publish'
    # 排序.
    ordering = ('status', 'publish')
