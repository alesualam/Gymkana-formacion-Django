from django.db import models

from django.core.validators import FileExtensionValidator

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

defim = BASE_DIR + '/images/image.jpg'


# Create your models here.

class BaseItems(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    subtitle = models.CharField(max_length=50, blank=False, null=False)
    body = models.TextField(blank=False, null=False)

    class Meta:
        abstract = True


class New(BaseItems):
    publish_date = models.DateTimeField(auto_now_add=True, blank=True)
    image = models.ImageField(upload_to='images/', default=defim, validators=[FileExtensionValidator(['jpg', 'png'])])


class Event(BaseItems):
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)