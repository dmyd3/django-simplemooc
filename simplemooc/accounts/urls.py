from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.contrib.auth import views as auth_views

app_name='accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entrar/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('sair/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('registrar/', views.register, name='register'),
    path('registrar/', views.register, name='register'),
    path('editar/', views.edit, name='edit'),
    path('editar_senha/', views.edit_password, name='edit_password'),
    path('reset_senha', views.password_reset, name='password_reset'),
    re_path(r'^confirmar_senha/(?P<key>\w+)/$', views.password_reset_confirm, name='password_reset_confirm'),
]

