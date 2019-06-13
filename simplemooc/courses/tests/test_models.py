from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from simplemooc.courses.models import Courses
from model_mommy import mommy

class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.courses = mommy.make('courses.Courses', 
            name='Python na Web com Django', _quantity=10)
        self.courses = mommy.make('courses.Courses', 
            name='Python para Devs', _quantity=10)

        self.client = Client()

    def tearDown(self):
        Courses.objects.all().delete()
    
    def test_course_search(self):
        search = Courses.objects.search('django')
        self.assertEqual( len(search), 10 )
        search = Courses.objects.search('devs')
        self.assertEqual( len(search), 10 )