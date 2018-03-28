# -*- coding: utf-8 -*-
"""High level support for doing this and that."""
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import Http404
from .models import Event, New
from .forms import NewsForm


def index(request):

    """High level support for doing this and that."""
    latest_events_list = Event.objects.order_by('-start_date')[:3]
    latest_news_list = New.objects.order_by('-publish_date')[:3]
    context = {
        'latest_events_list': latest_events_list,
        'latest_news_list': latest_news_list,
    }

    return render(request, 'baseItems/index.html', context)


def detail_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    return render(request, 'baseItems/detailEvent.html', {'event': event})


def detail_new(request, new_id):
    try:
        new = New.objects.get(pk=new_id)
    except New.DoesNotExist:
        raise Http404("New does not exist")

    return render(request, 'baseItems/detailNew.html', {'new': new})


def show_news(request):
    news = New.objects.order_by("-publish_date")
    context = {
        'news': news
    }
    return render(request, 'baseItems/news.html', context)


def new_create_v1(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            news = New.objects.all()
            return render(request, 'baseItems/news.html', {'news': news})
    else:
        form = NewsForm()
    return render(request, 'baseItems/newCreate.html', {'form': form})
