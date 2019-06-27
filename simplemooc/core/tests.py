from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.urls import reverse

# Create your tests here.
class HomeViewTest(TestCase):
    
    def test_home_status_code(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        #testa se o status eh igual a 200

    def test_home_template_used(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'home.html')
        #testa se o template usado eh o 'home.html'
