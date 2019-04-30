from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.contrib.auth import views as auth_views

app_name='accounts'

urlpatterns = [
    path('entrar/', auth_views.LoginView.as_view(), name='login'),
    path('sair/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('registrar/', views.register, name='register'),
]

