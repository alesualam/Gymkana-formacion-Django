# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class BaseItems(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    subtitle = models.CharField(max_length=200, blank=False, null=False)
    body = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class New(BaseItems):
    publish_date = models.DateField()
    image = models.ImageField(upload_to="img")


class Event(BaseItems):
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
