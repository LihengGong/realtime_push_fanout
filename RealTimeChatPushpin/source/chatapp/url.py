from django.urls import path, re_path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    re_path(r'^messages/(?P<room_name>\w+)/$', views.chat_messages, name='get-chat-messages'),
    path('register/', views.user_register, name='register'),
]
