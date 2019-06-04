from django.db import models
from django.urls import reverse
from django.conf import settings

from simplemooc.core.mail import send_mail_template

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
            models.Q(status__icontains=query) |
            models.Q(user__icontains=query) 
            )

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
    
    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name= 'Inscrição'
        verbose_name_plural = 'Incrições'
        unique_together= ( ('user','course'), )
        #o unique_together define q só pode exister um conjunto unico
        #de usuario e curso, evitando repetições

class Announcement(models.Model):

    course = models.ForeignKey( Courses, on_delete=models.DO_NOTHING, 
        verbose_name='Curso', related_name='announcements')
    title = models.CharField( 'Título', max_length=100 )
    content = models.TextField('Conteúdo')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True) 

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Anúncio"
        verbose_name_plural = "Anúncios"
        ordering = ['-created_at']

class Comment(models.Model):

    announcement = models.ForeignKey(Announcement, verbose_name='Anúncio',
        on_delete=models.DO_NOTHING, related_name='comments'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, 
                            verbose_name='usuário')
    comment = models.TextField('Comentário')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

def post_save_announcement(instance, created, **kwargs):
    subject = instance.title
    context = {
        'announcement':instance,
    }
    template_name = 'courses/announcement_mail.html'
    enrollments = Enrollment.objects.filter(
        course=instance.course
    )
    for enrollment in enrollments:
        recipient_list = [enrollment.user.email]
        send_mail_template( subject, template_name, context, recipient_list )

models.signals.post_save.connect(
    post_save_announcement, sender=Announcement, dispatch_uid='post_save_announcement'
)

class Lesson(models.Model):

    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank = True)
    number = models.IntegerField('Número(ordem)', blank=True, default=0)
    release_date = models.DateField('Data de liberação', blank=True, null=True)

    course = models.ForeignKey(Courses, on_delete=models.DO_NOTHING,
        verbose_name='Curso', related_name='lessons')

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Aulas"
        verbose_name_plural = "Aulas"
        ordering = ['number']

class Material(models.Model):

    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Vídeo Embutido(embedded', blank=True)
    file = models.FileField('Arquivo', upload_to='lessons/materials',
        blank=True, null=True)
    
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING,
        verbose_name='aula', related_name='materials')

    def is_embedded(self):
        return bool(self.embedded)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Material'
        verbose_name_plural='Materiais'