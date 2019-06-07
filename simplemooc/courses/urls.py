from django.urls import path, include, re_path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    #re_path(r'^(?P<pk>\d+)/$', views.details, name='details'),
    re_path(r'^(?P<slug>[\w_-]+)/$', views.details, name='details'),
    re_path(r'^(?P<slug>[\w_-]+)/inscricao$', views.enrollment, name='enrollment'),
    re_path(r'^(?P<slug>[\w_-]+)/cancelar_inscricao$', views.undo_enrollment, 
        name='undo_enrollment'),
    re_path(r'^(?P<slug>[\w_-]+)/anuncios$', views.announcements, name='announcements'),
    re_path(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$', views.show_announcement, name='show_announcement'),
    re_path(r'^(?P<slug>[\w_-]+)/aulas/$', views.lessons, name='lessons'),
    re_path(r'^(?P<slug>[\w_-]+)/aulas/(?P<pk>\d+)/$', views.lesson, name='lesson'),
    re_path(r'^(?P<slug>[\w_-]+)/materiais/(?P<pk>\d+)/$', views.material, name='material'),
]