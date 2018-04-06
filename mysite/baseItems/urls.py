from django.conf.urls import url
from . import views

app_name = 'baseItems'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^events/(?P<event_id>\d+)/$', views.detail_event, name='detailEvent'),
    url(r'^news/(?P<new_id>\d+)/$', views.detail_new, name='detailNew'),
    url(r'^v1/news/$', views.show_news, name='news'),
    url(r'^v1/new/create/$', views.new_create_v1, name='createNew'),
    url(r'^v1/new/update/(?P<new_id>\d+)/$', views.new_update_v1, name='updateNew'),
    url(r'^v1/new/delete/(?P<new_id>\d+)/$', views.new_delete_v1, name='deleteNew'),
    url(r'^v2/news/$', views.ShowNews.as_view(), name='newsClass'),
    url(r'^v2/new/create/$', views.NewCreate.as_view(), name='createNewClass'),
    url(r'^v2/new/update/(?P<pk>\d+)/$', views.NewUpdate.as_view(), name='updateNewClass'),
    url(r'^v2/new/delete/(?P<pk>\d+)/$', views.NewDelete.as_view(), name='deleteNewClass'),
    url(r'^v2/events/$', views.ShowEvents.as_view(), name='eventsClass'),
    url(r'^v2/event/create/$', views.EventCreate.as_view(), name='createEventClass'),
    url(r'^v2/event/update/(?P<pk>\d+)/$', views.EventUpdate.as_view(), name='updateEventClass'),
    url(r'^v2/event/delete/(?P<pk>\d+)/$', views.EventDelete.as_view(), name='deleteEventClass'),
]
