# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager

class Thread(mode.Model):

    title = models.CharField('Título', max_length=100)
    body - models.TextField(u'Mensagem')
    author = models.ForeignKey(
        settigs.AUTH_USER_MODEL, verbose_name ='Autor', related_name='threads'
    )
    views = models.IntegerField('Visualizações', blanj=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)
    tags = TaggableManager()

    created_at = models.DateTimeField('Criado em:',auto_now_add=True )
    modified = models.DateTimeField('Modificado em:',auto_now=True )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']
    
class Reply(models.Model):

    reply - models.TextField('Resposta')
    author = models.ForeignKey(
        settigs.AUTH_USER_MODEL, verbose_name ='Autor', related_name='replies'
    )
    correct = models.BooleanField('Correta?', blank=True, default=False)

    created_at = models.DateTimeField('Criado em:',auto_now_add=True )
    modified = models.DateTimeField('Modificado em:',auto_now=True )

    def __str__(self):
        return self.reply[:100]
    
    class Meta:
        verbose_name= 'Resposta'
        verbose_name_plural= 'Respostas'
        ordering = ['correct','created']