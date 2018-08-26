from django.conf.urls import url
from django_liveresource import views

urlpatterns = [
    url(r'^multi/$', views.multi, name='multi'),
    url(r'^updates/$', views.updates, name='updates'),
    url(r'^socket/usera$', views.echo_usera, name='usera'),
    url(r'^socket/userb$', views.echo_userb, name='userb'),
    url(r'^socket/broadcast$', views.broadcast, name='broadcast'),
]
