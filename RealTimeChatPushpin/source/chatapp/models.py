from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Room(models.Model):
    room_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    text = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_messages')

    def __str__(self):
        return '{}|{}|{}: {}'.format(self.room, self.author,
                                     self.time_stamp.strftime('%Y-%m-%d %H:%M'), self.text)

    class Meta:
        ordering = ['time_stamp']
