# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     urls.py  
   Description :  
   Author :       JHao
   date：          2017/4/13
-------------------------------------------------
   Change Activity:
                   2017/4/13: 
-------------------------------------------------
"""
__author__ = 'JHao'

from blog import views
from django.conf.urls import url

urlpatterns = [
    url(r'^hello/$', views.Hello, name='hello'),
    url(r'^index/$', views.Index, name='index'),
    url(r'^about/$', views.About, name='about'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^link/$', views.Link, name='link'),
    url(r'^message$', views.Message, name='message'),
    url(r'^article/(?P<pk>\d+)/$', views.Articles, name='article'),
    url(r'^api/getarticle/(?P<pk>\d+)/$', views.GetArticle, name='api/getarticle'),
    url(r'^api/uploadarticle/$', views.UploadArticle, name='api/uploadarticle'),
    url(r'^api/downloadarticle/$', views.DownloadArticle, name='api/downloadarticle'),
    url(r'^get_comment/$', views.GetComment, name='get_comment'),
    url(r'^detail/(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^detail/(?P<pk>\d+)$', views.detail, name='detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^tag/(?P<name>.*?)/$', views.tag, name='tag'),
    
]
