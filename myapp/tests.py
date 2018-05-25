from django.test import TestCase

from myapp.models import New, Event
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings


from .forms import PostForm

class htmlTests(TestCase):

    def test_index(self):
        # Index without news test
        response = self.client.get(reverse('myapp:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No news found.')
        self.assertQuerysetEqual(response.context['latest_news'], [])

        # Index with news test, only showing the latest 3
        for i in range(4):
            New.objects.create(title='title' + str(i), subtitle='subtitle' + str(i), body='body' + str(i))

        response = self.client.get(reverse('myapp:index'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'title0')
        self.assertContains(response, 'title1')
        self.assertContains(response, 'title2')
        self.assertContains(response, 'title3')


    def test_news_list(self):
        # Empty news list test
        response = self.client.get(reverse('myapp:news_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The list is empty')
        self.assertQuerysetEqual(response.context['news_list'], [])

        # News list that shows every new
        for i in range(4):
            New.objects.create(title='title' + str(i), subtitle='subtitle' + str(i), body='body' + str(i))

        response = self.client.get(reverse('myapp:news_list'))
        self.assertEquals(response.status_code, 200)

        for i in range(4):
            self.assertContains(response, 'title' + str(i))


    def test_news_create(self):
        response = self.client.get(reverse('myapp:create'))

        # Correct form test with all fields and no image (default image used)
        count = New.objects.count()
        form_data = {'title': 'title1', 'subtitle': 'subtitle1', 'body': 'body1'}
        response = self.client.post(reverse('myapp:create'), data=form_data, files='')
        form = PostForm(data=form_data)
        count = count + 1
        self.assertEqual(settings.IMAGE_DEFAULT, New.objects.get(pk=1).image.name)
        self.assertTrue(form.is_valid())
        self.assertEquals(count, New.objects.count())
        self.assertEqual(response.status_code, 302)

        # Correct form test with all fields and custom image chosen by the user
        form_data = {'title': 'title1', 'subtitle': 'subtitle1', 'body': 'body1'}
        img = open(settings.IMAGE_DEFAULT, 'rb')
        file = SimpleUploadedFile(img.name, img.read())
        response = self.client.post(reverse('myapp:create'), data=form_data, files={'image': file})
        form = PostForm(data=form_data, files={'image': file})
        count = count + 1
        self.assertEquals(count, New.objects.count())
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 302)

        # Incorrect form test without data
        form_data = {}
        response = self.client.post(reverse('myapp:create'), data=form_data)
        form = PostForm(data=form_data)

        self.assertFalse(form.is_valid())
        #self.assertFormError(response, '', 'title', 'Completa este campo')
        self.assertEqual(count, New.objects.count())

        # Incorrect form test due to large image file
        form_data = {'title': 'hola', 'subtitle': 'quetal', 'body': 'body1'}
        img = open('/home/asuarez/test/large_image.jpg', 'rb')  # Duda
        file = SimpleUploadedFile(img.name, img.read())
        import ipdb;ipdb.set_trace()
        response = self.client.post(reverse('myapp:create'), follow=True, data=form_data, files={'image': file})
        #response = self.client.post(reverse('myapp:create'), data=form_data, files={'image': file})

        import ipdb;ipdb.set_trace()
        self.assertContains(response, "Image file too large ( > 10mb )")
        self.assertEqual(response.status_code, 302)


    def test_news_detail(self):

        # Test getting an existing new
        New.objects.create(title='title1', subtitle='subtitle1', body='body1')
        response = self.client.get(reverse('myapp:new_detail', kwargs={'new_id': 1}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'title1')

        # Test getting a new that wasn't created
        response = self.client.get(reverse('myapp:new_detail', kwargs={'new_id': 2}))
        self.assertEqual(response.status_code, 404)


    def test_new_update(self):

        # Updating an existing new
        New.objects.create(title='title1', subtitle='subtitle1', body='body1')
        response = self.client.get(reverse('myapp:new_update', kwargs={'new_id': 1}))
        self.assertContains(response, 'title1')
        form_data = {'title': 'title2', 'subtitle': 'subtitle2', 'body': 'body2'}
        form = PostForm(data=form_data)
        response = self.client.post(reverse('myapp:new_update', kwargs={'new_id': 1}), data=form_data, files='')

        self.assertEquals(response.status_code, 302)
        self.assertTrue(form.is_valid())

        response = self.client.get(reverse('myapp:news_list'))
        self.assertContains(response, 'title2')
        self.assertNotContains(response, 'title1')

        # Updating a new that wasn't created
        response = self.client.get(reverse('myapp:new_update', kwargs={'new_id': 0}))
        self.assertEqual(response.status_code, 404)


    def test_new_delete(self):

        # Deleting a new
        New.objects.create(title='title1', subtitle='subtitle1', body='body1')
        response = self.client.get(reverse('myapp:new_delete', kwargs={'new_id': 1}))

        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('myapp:news_list'))
        self.assertNotContains(response, 'title1')

        # Deleting a new that wasn't created
        response = self.client.get(reverse('myapp:new_delete', kwargs={'new_id': 1}))
        self.assertEquals(response.status_code, 404)
