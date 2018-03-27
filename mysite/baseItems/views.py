# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import Http404
from .models import Event, New


def index(request):
    latest_events_list = Event.objects.order_by('-start_date')[:3]
    latest_news_list = New.objects.order_by('-publish_date')[:3]
    context = {
        'latest_events_list': latest_events_list,
        'latest_news_list': latest_news_list,
    }

    return render(request, 'baseItems/index.html', context)


def detailEvent(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    return render(request, 'baseItems/detailEvent.html', {'event': event})


def detailNew(request, new_id):
    try:
        new = New.objects.get(pk=new_id)
    except New.DoesNotExist:
        raise Http404("New does not exist")

    return render(request, 'baseItems/detailNew.html', {'new': new})


def image(request):
    new = New()
    variables = RequestContext(request, {'new': new})
    return render_to_response('image.html', variables)
