# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from .models import New


class NewTestCase(TestCase):

    def test_empy_index(self):
        response = self.client.get(reverse("baseItems:index"))
        self.assertEqual(response.status_code, 200)
        num_news = New.objects.count()
        if num_news == 0:
            self.assertContains(response, "No news are available")
            self.assertQuerysetEqual(response.context['latest_news_list'], [])

    def test_no_news(self):
        response = self.client.get(reverse("baseItems:detailNew"))
        New.objects.create(id=0, title="noticiatest", subtitle="subtitulotest", body="cuerpazotest")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "New does not exist")

    def test_index(self):
        response = self.client.get(reverse("baseItems:index"))
        self.assertEqual(response.status_code, 200)

    def test_list_news(self):
        response = self.client.get(reverse("baseItems:news"))
        self.assertEqual(response.status_code, 200)

    def test_detail_news(self):
        new_test = New.objects.create(title="noticiatest", subtitle="subtitulotest", body="cuerpazotest")
        response = self.client.get(reverse("baseItems:detailNew", kwargs={"new_id": new_test.pk}))
        self.assertEqual(response.status_code, 200)

    def test_create_news_post_function(self):
        num_news_bef = New.objects.count()
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        url = reverse("baseItems:createNew")
        data = {"title": "crearnoticiatest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}
        nu = self.client.post(url, data)
        self.assertEqual(nu.status_code, 302)
        num_news_aft = New.objects.count()
        self.assertEqual(num_news_aft, num_news_bef + 1)

    def test_create_news_get_function(self):
        num_news_bef = New.objects.count()
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        url = reverse("baseItems:createNew")
        import ipdb;ipdb.set_trace()
        data = {"title": "crearnoticiatest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}
        nu = self.client.get(url, data)
        self.assertEqual(nu.status_code, 200)
        num_news_aft = New.objects.count()
        self.assertEqual(num_news_aft, num_news_bef + 1)

    def test_create_news_class(self):
        num_news_bef = New.objects.count()
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        url = reverse("baseItems:createNewClass")
        data = {"title": "crearnoticiatest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}
        n = self.client.post(url, data)
        self.assertEqual(n.status_code, 302)
        num_news_aft = New.objects.count()
        self.assertEqual(num_news_aft, num_news_bef + 1)

    def test_create_news_function_wrong_format(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/17888.gif', 'rb')
        url = reverse("baseItems:createNew")
        data = {"title": "crearnoticiamaltest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}
        n = self.client.post(url, data)
        self.assertEqual(n.status_code, 200)
        self.assertContains(n, "Wrong format, only jpg, jpeg, png")
        '''Al ser 200 no redirecciona y sigue en la misma pagina esperando que le introduzca una imagen valida'''

    def test_create_news_function_heavy(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/high-resolution-image-7.jpg', 'rb')
        url = reverse("baseItems:createNew")
        data = {"title": "crearnoticiamaltest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}
        n = self.client.post(url, data)
        self.assertEqual(n.status_code, 200)
        self.assertContains(n, "Too heavy image, less than 10 MB please")
        '''Al ser 200 no redirecciona y sigue en la misma pagina esperando que le introduzca una imagen valida'''

    def test_update_post_funciones(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        new = New.objects.create(title="creanoticiatest", subtitle="subtitulotest", body="cuerpazotest")
        num_elem_bef = New.objects.count()
        url = reverse("baseItems:updateNew", kwargs={"new_id": new.pk})
        data = {"title": "updatenew", "subtitle": "updatenew", "body": "updatebody", "image": upload_file}
        n = self.client.post(url, data)
        self.assertEqual(n.status_code, 302)
        num_elem_aft = New.objects.count()
        self.assertEqual(num_elem_aft, num_elem_bef)

    def test_update_get_funciones(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        new = New.objects.create(title="creanoticiatest", subtitle="subtitulotest", body="cuerpazotest")
        num_elem_bef = New.objects.count()
        url = reverse("baseItems:updateNew", kwargs={"new_id": new.pk})
        data = {"title": "updatenew", "subtitle": "updatenew", "body": "updatebody", "image": upload_file}
        n = self.client.get(url, data)
        self.assertEqual(n.status_code, 200)
        num_elem_aft = New.objects.count()
        self.assertEqual(num_elem_aft, num_elem_bef)

    def test_update_post_class(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        new = New.objects.create(title="creanoticiatest", subtitle="subtitulotest", body="cuerpazotest")
        num_elem_bef = New.objects.count()
        url = reverse("baseItems:updateNewClass", kwargs={"pk": new.pk})
        data = {"title": "updatenew", "subtitle": "updatenew", "body": "updatebody", "image": upload_file}
        n = self.client.post(url, data)
        self.assertEqual(n.status_code, 302)
        num_elem_aft = New.objects.count()
        self.assertEqual(num_elem_aft, num_elem_bef)

'''
class EventTestCase(TestCase):
    def setUp(self):
        start_date = timezone.now()
        end_date = timezone.now()
        Event.objects.create(title="eventotest", subtitle="subtitulotest", body="cuerpotest", start_date=start_date, end_date=end_date)

    def test_index(self):
        response = self.client.get(reverse("baseItems:index"))
        self.assertEqual(response.status_code, 200)

    def test_detail_events(self):
        start_date = timezone.now()
        end_date = timezone.now()
        event_test = Event.objects.get(title="eventotest", subtitle="subtitulotest", body="cuerpotest", start_date=start_date, end_date=end_date)
        response = self.client.get(reverse("baseItems:detailEvent", kwargs={"event_id": event_test.pk}))
        self.assertEqual(response.status_code, 200)
'''
