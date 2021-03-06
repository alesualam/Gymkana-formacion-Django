# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import New, Event

# Register your models here.


class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'publish_date')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'start_date', 'end_date')


admin.site.register(New, NewAdmin)

admin.site.register(Event, EventAdmin)
