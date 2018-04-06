# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from .models import Event, New
from .forms import EventsForm, NewsForm


def index(request):

    latest_events_list = Event.objects.order_by('end_date')[:3]
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
            return redirect('baseItems:news')
    else:
        form = NewsForm()

    return render(request, 'baseItems/newCreate.html', {'form': form})


def new_update_v1(request, new_id):
    new = get_object_or_404(New, pk=new_id)
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=new)
        if form.is_valid():
            form.save()
            return redirect('baseItems:news')
    else:
        form = NewsForm(instance=new)
    return render(request, 'baseItems/newUpdate.html', {'form': form})


def new_delete_v1(request, new_id):
    new = get_object_or_404(New, pk=new_id)
    if request.method == "POST":
        new.delete()
        return redirect('baseItems:news')

    context = {
        'new': new
    }
    return render(request, 'baseItems/confirmDelete.html', context)


class ShowNews(ListView):
    model = New
    template_name = 'baseItems/news.html'
    context_object_name = 'news'

    def get_queryset(self):
        return self.model.objects.order_by("-publish_date")


class NewCreate(CreateView):
    form_class = NewsForm
    template_name = 'baseItems/newCreate.html'
    model = New

    def get_success_url(self):
        return reverse('baseItems:newsClass')


class NewUpdate(UpdateView):
    form_class = NewsForm
    template_name = 'baseItems/newUpdate.html'
    model = New

    def get_success_url(self):
        return reverse('baseItems:newsClass')


class NewDelete(DeleteView):
    model = New

    success_url = reverse_lazy('baseItems:newsClass')


class ShowEvents(ListView):
    model = Event
    template_name = 'baseItems/events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return self.model.objects.order_by("end_date")


class EventCreate(CreateView):
    form_class = EventsForm
    template_name = 'baseItems/eventCreate.html'
    model = Event

    def get_success_url(self):
        return reverse('baseItems:eventsClass')


class EventUpdate(UpdateView):
    form_class = EventsForm
    template_name = 'baseItems/eventUpdate.html'
    model = Event

    def get_success_url(self):
        return reverse('baseItems:eventsClass')


class EventDelete(DeleteView):
    model = Event

    success_url = reverse_lazy('baseItems:eventsClass')
