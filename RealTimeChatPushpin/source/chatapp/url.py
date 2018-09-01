from django.urls import path, re_path, include
from . import views


urlpatterns = [
    path('', views.user_login),
    re_path(r'^login/', views.user_login, name='login'),
    re_path(r'^messages/(?P<room_name>\w+)/$', views.chat_messages, name='get-chat-messages'),
    re_path(r'^register/', views.user_register, name='register'),
    re_path(r'^events/', include('django_eventstream.urls')),
]
