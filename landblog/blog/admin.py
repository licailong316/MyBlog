from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Category, Tag, Article


# 分类管理
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ['name', 'parent', 'created_at', 'post_count', 'author']
    # 编辑页可编辑字段（owner 和 created_at 通常是自动设置的，避免人为修改）
    fields = ('name', 'parent')

    def post_count(self, obj):
        # 获取该分类下的文章数量（默认反向关系为 article_set）
        return obj.article_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


# 标签管理
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ['name', 'created_at', 'post_count', 'author']
    # 编辑页可编辑字段
    fields = ('name',)

    def post_count(self, obj):
        # 获取该分类下的文章数量（默认反向关系为 article_set）
        return obj.article_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器只展示当前用户分类
    """
    title = '分类过滤器'
    parameter_name = 'author_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(author=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


# 文章管理
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 列表显示字段
    list_display = ['title', 'category', 'created_at', 'operator', 'author']
    # 设置点击哪一列可以进入编辑页
    list_display_links = ['title']

    # 分类过滤器
    list_filter = [CategoryOwnerFilter]

    # 搜索字段
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = False

    # 分组字段显示，优化编辑页面结构
    fieldsets = (
        ('基础配置', {
            'description': '设置文章标题与分类',
            'fields': ('title', 'category'),
        }),
        ('内容', {
            'fields': ('desc', 'content'),
        }),
        ('额外信息', {
            'classes': ('collapse',),  # 可折叠
            'fields': ('tags', 'is_top'),  # 正确字段为 tags（多对多）
        }),
    )

    def operator(self, obj):
        # 自定义操作列：编辑按钮（指向默认 admin 修改页面）
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_article_change', args=(obj.id,)),  # 注意 admin 命名空间
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(ArticleAdmin, self).save_model(request, obj, form, change)
