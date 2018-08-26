from django.urls import include, path, re_path
import django_eventstream
from . import views

urlpatterns = [
    re_path(r'^$', views.home),
    re_path(r'^(?P<room_id>[^/]+)$', views.home),
    re_path(r'^rooms/(?P<room_id>[^/]+)/messages/$', views.messages),
    re_path(r'^events/', include(django_eventstream.urls)),
]
