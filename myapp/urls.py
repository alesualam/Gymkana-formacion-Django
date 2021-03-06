from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^v1/news/create/$', views.create, name='create'),
    url(r'^v1/news/$', views.news_list, name='news_list'),
    url(r'^v1/news/(?P<new_id>\d+)/$', views.new_detail, name='new_detail'),
    url(r'^v1/news/update/(?P<new_id>\d+)/$', views.new_update, name='new_update'),
    url(r'^v1/news/delete/(?P<new_id>\d+)/$', views.new_delete, name='new_delete'),
    url(r'^v2/events/create/$', views.CreateEvent.as_view(), name='event_create'),
    url(r'^v2/events/$', views.EventsList.as_view(), name='events_list'),
    url(r'^v2/events/(?P<pk>\d+)/$', views.EventDetail.as_view(), name='events_detail'),
    url(r'^v2/events/update/(?P<pk>\d+)/$', views.EventUpdate.as_view(), name='event_update'),
    url(r'^v2/events/delete/(?P<pk>\d+)/$', views.EventDelete.as_view(), name='event_delete')
]
