# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


class BaseItems(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    subtitle = models.CharField(max_length=200, blank=False, null=False)
    body = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class New(BaseItems):
    publish_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="img", default='/img/periodico.jpg')


class Event(BaseItems):
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)


@receiver(post_delete, sender=New)
def delete_img(sender, **kwargs):
    try:
        image = kwargs.get('instance').image
        if image.name != "/img/periodico.jpg":
            os.remove(image.path)
    except OSError:
        pass
