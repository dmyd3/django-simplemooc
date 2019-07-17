# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager

from django_extensions.db.fields import AutoSlugField
from django.urls import reverse


class Thread(models.Model):

    title = models.CharField('Título', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    #slug = AutoSlugField('Identificador', max_length=100, unique=True, populate_from='title' )

    body = models.TextField('Mensagem')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        verbose_name ='Autor', related_name='threads'
    )
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)
    tags = TaggableManager()

    created_at = models.DateTimeField('Criado em:',auto_now_add=True )
    modified = models.DateTimeField('Modificado em:',auto_now=True )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread',args=[self.slug] )
    

    class Meta:
        verbose_name='Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']
    
class Reply(models.Model):

    thread = models.ForeignKey(
        Thread, on_delete=models.DO_NOTHING,
        verbose_name='Tópico', related_name='replies'
    )
    reply = models.TextField('Resposta')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
        verbose_name ='Autor', related_name='replies'
    )
    correct = models.BooleanField('Correta?', blank=True, default=False)

    created_at = models.DateTimeField('Criado em:',auto_now_add=True )
    modified = models.DateTimeField('Modificado em:',auto_now=True )

    def __str__(self):
        return self.reply[:100]
    
    class Meta:
        verbose_name= 'Resposta'
        verbose_name_plural= 'Respostas'
        ordering = ['correct','created_at']

def post_save_reply(created_at, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save() 
    # if created_at:
    #     instance.thread.answers = instance.thread.answers + 1
    #     instance.thread.save()

def post_delete_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    #instance.thread.answers = instance.thread.answers - 1
    instance.thread.save()

models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)
models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid='post_delete_reply'
)


