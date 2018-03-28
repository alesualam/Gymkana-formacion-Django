from django.conf.urls import url
from . import views

app_name = 'baseItems'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^events/(?P<event_id>\d+)/$', views.detail_event, name='detailEvent'),
    url(r'^news/(?P<new_id>\d+)/$', views.detail_new, name='detailNew'),
    url(r'^v1/news/$', views.show_news, name='news'),
    url(r'^v1/new/create/$', views.new_create_v1, name='createNew'),
]
