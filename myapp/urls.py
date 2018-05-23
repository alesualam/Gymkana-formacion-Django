from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^v1/news/create/$', views.create, name='create'),
    url(r'^v1/news/$', views.news_list, name='news_list'),
    url(r'^v1/news/(?P<new_id>\d+)/$', views.new_detail, name='new_detail')
]
