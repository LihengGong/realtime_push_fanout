from django.conf.urls import url
from . import consumers


websocket_urlpatterns = [
    url(r'^ws/sock/(?P<name>[^/]+)/$', consumers.StatConsumer),
]
