from django.urls import path, include, re_path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^tag/(?P<tag>[\w_-]+)$', views.index, name='index_tagged'),
    re_path(r'^(?P<slug>[\w_-]+)$', views.thread, name='thread'),
]