#!/user/bin/env python
#-*- coding:utf8 -*-
#@TIME   :2018/4/1 15:29
#@Author :weige
#@File :forms.py

from django import forms
from articles.models import ArticleColumn, ArticlePost, Comment, ArticleTag


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title","body")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commentator','body')

class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields =('tag',)