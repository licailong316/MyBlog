from django import forms

from .models import Category, Tag, Article


class ArticleAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label="摘要", required=False)