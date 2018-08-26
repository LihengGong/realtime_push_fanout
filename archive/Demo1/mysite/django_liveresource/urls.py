from django.conf.urls import url
from django_liveresource import views

urlpatterns = [
    url(r'^multi/$', views.multi, name='multi'),
    url(r'^updates/$', views.updates, name='updates'),
    url(r'^socket/$', views.echo, name='socket'),
]
