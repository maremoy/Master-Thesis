from django.conf.urls import include, url
from django.conf import settings
from django.contrib.staticfiles import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'survey'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^cancel/$', views.cancel, name='cancel'),
]