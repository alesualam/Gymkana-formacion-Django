from django.conf.urls import url
from . import views

app_name = 'baseItems'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^events/(?P<event_id>\d+)/$', views.detailEvent, name='detailEvent'),
    url(r'^news/(?P<new_id>\d+)/$', views.detailNew, name='detailNew'),
]
