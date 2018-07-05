#!/user/bin/env python
#-*- coding:utf8 -*-
#@TIME   :2018/3/22 18:51
#@Author :weige
#@File :urls.py
from django.conf.urls import url
from blog import views
app_name = 'blog'
urlpatterns = [
    url(r'^$',views.blog_title,name='blog_title'),
    url(r'(?P<article_id>\d)/$',views.blog_articles,name='article_content'),
]