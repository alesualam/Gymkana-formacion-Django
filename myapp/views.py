from __future__ import unicode_literals

from django.http import HttpResponse

from django.template import loader

from django.shortcuts import render

from django import forms

from .forms import PostForm

from .models import Event, New

from PIL import Image

# Create your views here.
def index(request):
    latest_news = New.objects.order_by('-publish_date')[:3]
    latest_events = Event.objects.order_by('-start_date')[:3]

    context = {
        'latest_news': latest_news,
        'latest_events': latest_events
    }

    return render(request, 'myapp/index.html', context)


def create(request):
    form = PostForm()
    form.fields['image'].initial = 'images/image.jpg'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = PostForm()

    return render(request, 'myapp/create.html', {'form': form})


def news_list(request):

    news_list = New.objects.order_by('-publish_date')

    context = {
        'news_list': news_list
    }

    return render(request, 'myapp/list.html', context)
