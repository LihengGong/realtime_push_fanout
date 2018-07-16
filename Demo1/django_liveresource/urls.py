from django.conf.urls import patterns, url
from django_liveresource import views

urlpatterns = patterns('',
	url(r'^multi/$', views.multi, name='multi'),
	url(r'^updates/$', views.updates, name='updates'),
)
