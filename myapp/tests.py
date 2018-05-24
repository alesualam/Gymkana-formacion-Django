from django.test import TestCase

from myapp.models import New, Event
from django.http import HttpRequest

from myapp import views
from myapp import urls

class IndexTests(TestCase):

    def test_index_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
