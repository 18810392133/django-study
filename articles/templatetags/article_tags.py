#!/user/bin/env python
#-*- coding:utf8 -*-
#@TIME   :2018/5/16 17:01
#@Author :weige
#@File :article_tags.py

from django import template

register = template.Library

from articles.models import ArticlePost


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()



