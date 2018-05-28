from __future__ import unicode_literals

from django.http import HttpResponse, Http404

from django.shortcuts import render, redirect

from django.conf import settings

from .forms import PostForm, C_Event

from .models import Event, New
from django.views import View


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
    form.fields['image'].initial = settings.IMAGE_DEFAULT

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')

    else:
        form = PostForm()

    return render(request, 'myapp/create.html', {'form': form})


def news_list(request):

    news_list = New.objects.order_by('-publish_date')

    context = {
        'news_list': news_list
    }

    return render(request, 'myapp/list.html', context)


def new_detail(request, new_id):

    try:
        new = New.objects.get(pk=new_id)
    except New.DoesNotExist:
        raise Http404("Can't get new")

    return render(request, 'myapp/n_detail.html', {'new': new})


def new_update(request, new_id):

    try:
        new = New.objects.get(pk=new_id)
    except New.DoesNotExist:
        raise Http404("Can't get new")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=new)
        if form.is_valid():
            form.save()
            return redirect('myapp:news_list')
    else:
        form = PostForm(instance=new)

    return render(request, 'myapp/create.html', {'form': form})


def new_delete(request, new_id):

    try:
        new = New.objects.get(pk=new_id)
    except New.DoesNotExist:
        raise Http404("Can't get new")

    instance = New.objects.get(id=new_id)
    instance.delete()

    news_list = New.objects.order_by('-publish_date')

    context = {
        'news_list': news_list
    }

    return render(request, 'myapp/list.html', context)

class CreateEvent(View):
    form_class = C_Event
    template_name = 'myapp/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')

        return render(request, self.template_name, {'form': form})
