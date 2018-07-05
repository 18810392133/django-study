#!/user/bin/env python
#-*- coding:utf8 -*-
#@TIME   :2018/5/22 23:27
#@Author :weige
#@File :urls.py

from django.conf.urls import url
from . import views
from image.views import CreateDongtaiView
app_name = 'image'


urlpatterns = [
    url(r'^list-images/$', views.list_images, name="list_images"),
    url(r'^create_new_dongtai/$',CreateDongtaiView.as_view(), name='create_new_dongtai'),
    url(r'^del-image/$', views.del_image, name='del_image'),
    url(r'^images/$', views.falls_images, name="falls_images"),
    url(r'^like_dongtai/$',views.like_dongtai,name="like_dongtai")
]

