from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from simplemooc.courses.models import Courses
from .forms import ContactCourse

class ContactCourseTestCase(TestCase):
    
    def setUp(self):
        self.course = Courses.objects.create(name='Django', slug='django')
        
    def tearDown(self):
        self.course.delete()
    
    # @classmethod
    # def setUpClass(cls):
    #     pass

    # @classmethod    
    # def tearDownClass(cls):
    #     pass
    
    def test_contact_form_error(self):
        data1 = {
            'name': 'Fulano de tal',
            'email':'as@email.com', 'message':'oioi'
            }
        
        client = Client()
        path = reverse('courses:details', args=[self.course.slug] )
        response = client.post(path, data1)
        
        form = ContactCourse(data=data1)
        self.assertTrue(form.is_valid())
        #verifica se o formulario está sendo valido, 
        # se os campos estiverem vazios, vai dar ERRO, como esperado.
        
        #self.assertFormError(response,'form', 'email', 'Please fill out this field.')
        #self.assertFormError(response,'form', 'message', 'Este campo é obrigatório.')
            
    def test_contact_form_success(self):
        data = {'name': 'Fulano de Tal', 'email': 'admin@admin.com', 'message':'Oi'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertEqual( len(mail.outbox), 1 )
        self.assertEqual( mail.outbox[0].to, [settings.CONTACT_EMAIL] )
