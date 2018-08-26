from django.urls import path
from .views import send_msg


urlpatterns = [
    path('send/', send_msg, name='send-msg'),
]
