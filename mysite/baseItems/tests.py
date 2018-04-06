# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from os import listdir
import datetime
from datetime import date, timedelta

from .models import Event, New


class NewTestCase(TestCase):

    def test_empy_index(self):
        response = self.client.get(reverse("baseItems:index"))
        self.assertEqual(response.status_code, 200)
        num_news = New.objects.count()

        if num_news == 0:
            self.assertContains(response, "No news are available")
            self.assertQuerysetEqual(response.context['latest_news_list'], [])

    def test_no_news(self):
        response = self.client.get(reverse("baseItems:detailNew", kwargs={"new_id": 0}))
        self.assertEqual(response.status_code, 404)

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

    def test_order_news(self):
        publish_date2 = timezone.now() + timezone.timedelta(days=-1)
        publish_date3 = timezone.now() + timezone.timedelta(days=-2)

        New.objects.create(title="noticiatest", subtitle="subtitulotest", body="cuerpazotest")
        noticia2 = New.objects.create(title="noticiatest2", subtitle="subtitulotest2", body="cuerpazotest2")
        noticia2.publish_date = publish_date2
        noticia2.save()
        noticia3 = New.objects.create(title="noticiatest3", subtitle="subtitulotest3", body="cuerpazotest3")
        noticia3.publish_date = publish_date3
        noticia3.save()

        response = self.client.get(reverse("baseItems:newsClass"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<ul>\n        \n            <li>\n                <a href="/news/1/">noticiatest <br/> subtitulotest</a>\n            </li>\n        \n            <li>\n                <a href="/news/2/">noticiatest2 <br/> subtitulotest2</a>\n            </li>\n        \n            <li>\n                <a href="/news/3/">noticiatest3 <br/> subtitulotest3</a>\n            </li>\n        \n    </ul>')

    def test_create_news_function(self):
        num_news_bef = New.objects.count()
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        url = reverse("baseItems:createNew")
        data = {"title": "crearnoticiatest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}

        create_new_get = self.client.get(url)
        self.assertEqual(create_new_get.status_code, 200)
        num_news_aft = New.objects.count()
        self.assertEqual(num_news_aft, num_news_bef)

        create_new_post = self.client.post(url, data)
        self.assertEqual(create_new_post.status_code, 302)
        num_news_aft = New.objects.count()
        self.assertEqual(num_news_aft, num_news_bef + 1)

    def test_create_news_class(self):
        num_news_bef = New.objects.count()
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        url = reverse("baseItems:createNewClass")
        data = {"title": "crearnoticiatest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}

        create_new_get = self.client.get(url)
        self.assertEqual(create_new_get.status_code, 200)
        num_news_aft = New.objects.count()
        self.assertEqual(num_news_aft, num_news_bef)

        create_new = self.client.post(url, data)
        self.assertEqual(create_new.status_code, 302)
        num_news_aft = New.objects.count()
        self.assertEqual(num_news_aft, num_news_bef + 1)

    def test_create_news_function_wrong_format(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/17888.gif', 'rb')
        url = reverse("baseItems:createNew")
        data = {"title": "crearnoticiamaltest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}

        create_new = self.client.post(url, data)
        self.assertEqual(create_new.status_code, 200)
        self.assertContains(create_new, "Wrong format, only jpg, jpeg, png")
        # Al ser 200 no redirecciona y sigue en la misma pagina esperando que le introduzca una imagen valida

    def test_create_news_function_heavy(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/high-resolution-image-7.jpg', 'rb')
        url = reverse("baseItems:createNew")
        data = {"title": "crearnoticiamaltest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}

        create_new = self.client.post(url, data)
        self.assertEqual(create_new.status_code, 200)
        self.assertContains(create_new, "Too heavy image, less than 10 MB please")
        # Al ser 200 no redirecciona y sigue en la misma pagina esperando que le introduzca una imagen valida

    def test_update_post_funciones(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        new = New.objects.create(title="creanoticiatest", subtitle="subtitulotest", body="cuerpazotest")
        num_elem_bef = New.objects.count()
        url = reverse("baseItems:updateNew", kwargs={"new_id": new.pk})
        data = {"title": "updatenew", "subtitle": "updatenew", "body": "updatebody", "image": upload_file}

        update_new_post = self.client.post(url, data)
        self.assertEqual(update_new_post.status_code, 302)
        num_elem_aft = New.objects.count()
        self.assertEqual(num_elem_aft, num_elem_bef)

    def test_update_get_funciones(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        new = New.objects.create(title="creanoticiatest", subtitle="subtitulotest", body="cuerpazotest")
        num_elem_bef = New.objects.count()
        url = reverse("baseItems:updateNew", kwargs={"new_id": new.pk})
        data = {"title": "updatenew", "subtitle": "updatenew", "body": "updatebody", "image": upload_file}

        update_new_get = self.client.get(url, data)
        self.assertEqual(update_new_get.status_code, 200)
        num_elem_aft = New.objects.count()
        self.assertEqual(num_elem_aft, num_elem_bef)

    def test_update_post_class(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/periodico.jpg', 'rb')
        new = New.objects.create(title="creanoticiatest", subtitle="subtitulotest", body="cuerpazotest")
        num_elem_bef = New.objects.count()
        url = reverse("baseItems:updateNewClass", kwargs={"pk": new.pk})
        data = {"title": "updatenew", "subtitle": "updatenew", "body": "updatebody", "image": upload_file}

        update_new = self.client.post(url, data)
        self.assertEqual(update_new.status_code, 302)
        num_elem_aft = New.objects.count()
        self.assertEqual(num_elem_aft, num_elem_bef)

    def test_delete_post_not_default_image(self):
        upload_file = open(settings.MEDIA_ROOT + '/img/indice.jpeg', 'rb')
        url = reverse("baseItems:createNew")
        data = {"title": "crearnoticiatest", "subtitle": "subtitulotest", "body": "cuerpazotest", "image": upload_file}

        self.client.post(url, data)
        new_test = New.objects.last()
        img_name = new_test.image.path.split("/")[-1]
        img_list = listdir(settings.MEDIA_ROOT + "/img/")

        self.assertTrue(img_name in img_list)
        url = reverse("baseItems:deleteNew", kwargs={"new_id": new_test.pk})
        new_delete = self.client.post(url)
        self.assertEqual(new_delete.status_code, 302)
        self.assertEqual(New.objects.count(), 0)


class EventTestCase(TestCase):
    def test_empy_index(self):
        response = self.client.get(reverse("baseItems:index"))
        self.assertEqual(response.status_code, 200)
        num_events = Event.objects.count()

        if num_events == 0:
            self.assertContains(response, "No events are available")
            self.assertQuerysetEqual(response.context['latest_events_list'], [])

    def test_index(self):
        response = self.client.get(reverse("baseItems:index"))
        self.assertEqual(response.status_code, 200)

    def test_list_events(self):
        response = self.client.get(reverse("baseItems:eventsClass"))
        self.assertEqual(response.status_code, 200)

    def test_detail_events(self):
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=+2)
        event_test = Event.objects.create(title="eventotest", subtitle="subtitulotest", body="cuerpotest", start_date=start_date, end_date=end_date)
        response = self.client.get(reverse("baseItems:detailEvent", kwargs={"event_id": event_test.pk}))
        self.assertEqual(response.status_code, 200)

    def test_no_events(self):
        response = self.client.get(reverse("baseItems:detailEvent", kwargs={"event_id": 0}))
        self.assertEqual(response.status_code, 404)

    def test_create_events(self):
        start_date = datetime.date.today()
        end_date = datetime.date.today()
        num_events_bef = Event.objects.count()
        url = reverse("baseItems:createEventClass")
        data = {"title": "eventotest2", "subtitle": "subtitulotest", "body": "cuerpotest", "start_date": start_date, "end_date": end_date}

        create_event_get = self.client.get(url)
        self.assertEqual(create_event_get.status_code, 200)
        num_events_aft = Event.objects.count()
        self.assertEqual(num_events_aft, num_events_bef)

        create_event = self.client.post(url, data)
        self.assertEqual(create_event.status_code, 302)
        num_events_aft = Event.objects.count()
        self.assertEqual(num_events_aft, num_events_bef + 1)

    def test_create_events_wrong_date(self):
        start_date = datetime.date.today()
        end_date = date.today() - timedelta(1)
        num_events_bef = Event.objects.count()
        url = reverse("baseItems:createEventClass")
        data = {"title": "eventotestmal", "subtitle": "subtitulotest", "body": "cuerpotest", "start_date": start_date, "end_date": end_date}

        create_event = self.client.post(url, data)
        self.assertEqual(create_event.status_code, 200)
        self.assertContains(create_event, "End date can&#39;t be before than start date")
        num_events_aft = Event.objects.count()
        self.assertEqual(num_events_aft, num_events_bef)

    def test_update_post_class(self):
        start_date = datetime.date.today()
        end_date = date.today() + timedelta(20)
        event = Event.objects.create(title="eventotestupdate", subtitle="subtitulotest", body="cuerpotest", start_date=start_date, end_date=end_date)
        num_elem_bef = Event.objects.count()

        start_date_update = datetime.date.today() + timedelta(10)
        end_date_update = date.today() + timedelta(30)
        url = reverse("baseItems:updateEventClass", kwargs={"pk": event.pk})
        data = {"title": "updateEvento", "subtitle": "subtitulotest", "body": "cuerpotest", "start_date": start_date_update, "end_date": end_date_update}

        update_event = self.client.post(url, data)
        self.assertEqual(update_event.status_code, 302)
        num_elem_aft = Event.objects.count()
        self.assertEqual(num_elem_aft, num_elem_bef)

    def test_delete_post_not_default_image(self):
        start_date = datetime.date.today()
        end_date = date.today() + timedelta(20)
        event = Event.objects.create(title="eventotestdelete", subtitle="subtitulotest", body="cuerpotest", start_date=start_date, end_date=end_date)
        url = reverse("baseItems:deleteEventClass", kwargs={"pk": event.pk})
        event_delete = self.client.post(url)
        self.assertEqual(event_delete.status_code, 302)
        self.assertEqual(Event.objects.count(), 0)
