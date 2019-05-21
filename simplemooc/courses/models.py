from django.db import models
from django.urls import reverse
from django.conf import settings


class CourseManager(models.Manager):
    
    def search(self, query): #realiza busca com base na string de entrada
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query) )


class Courses(models.Model):

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Atalho')
    description = models.TextField('Descricao simples', blank=True, max_length=80)
    about = models.TextField('Sobre o curso', blank=True)
    start_date = models.DateField('Data de Inicio', null=True, blank=True)
    image = models.ImageField(upload_to='courses/images', verbose_name='Imagem',
        null=True, blank=True)
    created_at = models.DateTimeField('Criado em:',auto_now_add=True )
    updated_at = models.DateTimeField('Atualizado em:',auto_now=True )

    objects = CourseManager()

    def get_absolute_url(self):
        #return ('courses:details', (), {'slug': self.slug} )
        return reverse('courses:details',args=[self.slug] )

    #href="{% url 'courses:details' course.slug %}"
    #<a href="{{ course.get_absolute_url }}">
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Curso"
        verbose_name_plural="Cursos"
        ordering = ['name'] #-name : decrescente

class EnrollmentManager(models.Manager):
    
    def search(self, query): #realiza busca com base na string de entrada
        return self.get_queryset().filter(
            models.Q(course__icontains=query) | 
            models.Q(status__icontains=query) )

class Enrollment(models.Model):

    STATUS_CHOICES = (
        (0,'Pendente'),(1,'Aprovado'),(2,'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Usuário",
        related_name="enrollments",
        on_delete =models.DO_NOTHING 
    )
    course = models.ForeignKey(
        Courses, verbose_name="Curso", related_name="enrollments",
        on_delete=models.DO_NOTHING
    )
    status = models.IntegerField('Situação',
        choices=STATUS_CHOICES, default=0, blank=True
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = EnrollmentManager()

    def active(self):
        self.status = 1
        self.save()

    class Meta:
        verbose_name= 'Inscrição'
        verbose_name_plural = 'Incrições'
        unique_together= ( ('user','course'), )
        #o unique_together define q só pode exister um conjunto unico
        #de usuario e curso, evitando repetições
