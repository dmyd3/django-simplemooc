from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings

import re
from django.core import validators

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField('Nome de Usuário', 
        max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile(r'^[\w.@+-]+$'),
        'Nome de usuario invalido, só pode conter @/./+/-/','invalid')]
        )
    email = models.EmailField('E-Mail', unique =True)
    first_name = models.CharField('Primeiro Nome', max_length=100, blank=True)
    last_name = models.CharField('Ultimo Nome', max_length=100, blank=True)
    #name = models.CharField('Nome', max_length=100, blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff= models.BooleanField('É da equipe', blank=True, default=False)
    date_joined = models.DateTimeField('Data de entrada', auto_now_add=True, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'username' #campo que será unico
    REQUIRED_FIELDS = ['email'] #necessario para criaçao de superuser

    def __str__(self):
        return self.first_name or self.username
    
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name+" "+self.last_name or "Nao informado"

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class PasswordReset(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,#Cascade deleta tudo relacionado ao usuario
        verbose_name='Usuário', 
        related_name="resets"
        )

    key = models.CharField("Chave", max_length=100, unique=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    confirmed = models.BooleanField("Confirmado?", default=False, blank=True)

    def __str__(self):
        return "{0} em {1}".format(self.user, self.created_at)
    
    class Meta:
        verbose_name = "Nova Senha"
        verbose_name_plural = "Novas Senhas"
        ordering = ['-created_at']










