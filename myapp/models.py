from django.db import models


# Create your models here.

class BaseItems(models.Model):
    title = models.CharField(max_length=50, blank=False)
    subtitle = models.CharField(max_length=50, blank=False)
    body = models.TextField(blank=False)


class New(BaseItems):
    publish_date = models.DateTimeField(auto_now_add=True, blank=True)
    image = models.ImageField(upload_to='image/', default='/gymk/miapp/image.jpg')


class Event(BaseItems):
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
