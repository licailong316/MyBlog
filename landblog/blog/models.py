from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    分类模型，支持多级分类结构
    - name: 分类名称
    - parent: 可选的上级分类
    - created_at: 创建时间（自动生成）
    """
    name = models.CharField(max_length=100, unique=True, help_text="分类名称", verbose_name="分类名称")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, help_text="可选的上级分类", verbose_name="父分类")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '分类'
        ordering = ['-id']

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    标签模型
    - name: 标签名称
    - created_at: 创建时间（自动生成）
    """
    name = models.CharField(max_length=30, unique=True, help_text="标签名称", verbose_name="标签名称")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '标签'
        ordering = ['-id']

    def __str__(self):
        return self.name

class Article(models.Model):
    """
    文章模型
    - title: 标题
    - summary: 摘要
    - content: 正文内容
    - author: 作者（关联用户）
    - category: 所属分类
    - tags: 文章标签
    - cover: 封面图
    - is_top: 是否置顶
    - view_count: 阅读量
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    title = models.CharField(max_length=200, verbose_name="标题")
    desc = models.TextField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name="分类")
    tags = models.ManyToManyField(Tag, verbose_name="标签")
    is_top = models.BooleanField(default=False, verbose_name="是否置顶")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ['-is_top', '-created_at']

    def __str__(self):
        return self.title


