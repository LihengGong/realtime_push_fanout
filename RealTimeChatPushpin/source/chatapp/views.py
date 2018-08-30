from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
# from rest_framework.decorators import api_view
# from rest_framework import status
from .forms import LoginForm, UserRegistrationForm, MessageForm
from .models import Message, Room


# Create your views here.
@require_http_methods(['GET', 'POST'])
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print('user_login-post: request.POST=', request.POST)
        print('user_login-post: form=', form)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(request,
                                username=cleaned_data['username'],
                                password=cleaned_data['password'])
            print('in user_login, user={}, type(user)={}'.format(user, type(user)))
            room_name = cleaned_data['room']
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/messages/{}/'.format(room_name))
    else:
        form = LoginForm()
    return render(request,
                  'chatapp/login.html',
                  {'form': form})


@require_http_methods(['GET', 'POST'])
def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['first_password']
            )
            new_user.save()
            return render(request,
                          'chatapp/register_done.html')
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'chatapp/register.html',
                  {'user_form': user_form})


@require_http_methods(['GET', 'POST'])
def chat_messages(request, room_name):
    prev_messages = []
    history_messages = []

    if request.method == 'GET':
        room_obj, created = Room.objects.get_or_create(room_name=room_name)
        print('chat_messages: request=', request)
        print('chat_messages: request.POST', request.POST)
        print('chat_messages: request.GET', request.GET)
        print('chat_messages: created=', created)
        print('chat_messages: room_obj=', room_obj)
        if not created:
            history_messages = room_obj.room_messages.all()[:50]
    else:
        # TODO broadcast the chat message to all clients in the same room
        print('chat_messages: request.POST=', request.POST)
        print('POST: room_name=', room_name)
        print('POST: request.session', request.session)
        print('POST: request.user', request.user)
        print('POST: type(request.user)=', type(request.user))
        cur_message = request.POST['message']
        room_obj = Room.objects.get(room_name=room_name)
        message = Message(author=request.user,
                          room=room_obj,
                          text=cur_message)
        message.save()
        print('POST: message=', message)
        history_messages = room_obj.room_messages.all()[:50]

    for message in history_messages:
        prev_messages.append('{}'.format(message))

    return render(request,
                  'chatapp/chatroom.html',
                  {'prev_messages': prev_messages,
                   'form': MessageForm()})
