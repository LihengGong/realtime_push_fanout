from django.urls import path, re_path, include
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream


urlpatterns = [
    re_path(r'^events/', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    )),
    re_path(r'', AsgiHandler),
]
