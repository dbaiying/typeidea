import xadmin
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


from xadmin.layout import Row, Fieldset, Container
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter


from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


# Register your models here.


# class PostInline(admin.TabularInline):  # 可选择继承自admin.StackedInline，以获取不同的展示样式
#     fields = ('title', 'desc')
#     extra = 1  # 控制额外多几个
#     model = Post


class PostInline:
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 1
    model = Post


# @admin.register(Category, site=custom_site)
@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')

    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


# @admin.register(Tag, site=custom_site)
@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器只展示当前用户分类"""

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


# title = '分类过滤器'
# parameter_name = 'owner_category'
#
# def lookups(self, request, model_admin):
#     return Category.objects.filter(owner=request.user).values_list('id', 'name')
#
# def queryset(self, request, queryset):
#     category_id = self.value()
#
#     if category_id:
#         return queryset.filter(category_id=self.value())
#     return queryset


# @admin.register(Post, site=custom_site)
@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator',
    ]
    list_display_links = []

    list_filter = ['category']  # 注意这里不是定义的filter类，而是字段名
    # list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    # fields = (
    #     'category',
    #     'title',
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    exclude = ['owner']

    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )
    # fieldsets = (
    #     ('基础配置', {
    #         'description': '基础配置描述',
    #         'fields': (
    #             ('title', 'category'),
    #             'status',
    #         ),
    #     }),
    #     ('内容', {
    #         'fields': (
    #             'desc',
    #             'content',
    #         ),
    #     }),
    #     ('额外信息', {
    #         'classes': ('wide',),
    #         'fields': ('tag',),
    #     })
    # )
    # filter_vertical = ('tag',)
    filter_horizontal = ('tag',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('cus_admin:blog_post_change', args=(obj.id,))
            reverse(self.model_admin_url('change', obj.id))
        )

    operator.short_description = '操作'

    # @property
    # def media(self):
    #     # xadmin基于Bootstrap,引入会导致页面样式冲突，这里只做演示
    #     media = super().media
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     })
    #     return media

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


# @admin.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message', ]
