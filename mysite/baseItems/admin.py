# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Event, New


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'start_date', 'end_date')


class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'publish_date')


admin.site.register(Event, EventAdmin)
admin.site.register(New, NewAdmin)
