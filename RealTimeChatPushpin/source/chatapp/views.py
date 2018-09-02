from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.core.serializers.json import DjangoJSONEncoder
from django_eventstream import send_event
import json
from .forms import LoginForm, UserRegistrationForm
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
                    # return redirect('/messages/{}/'.format(room_name))
                    print('user_login: login succeeds. Rendering chatroom now')
                    return render(request,
                                  'chatapp/chatroom.html',
                                  {'room_name': room_name})
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
    created = True

    if request.method == 'GET':
        room_obj, created = Room.objects.get_or_create(room_name=room_name)
    else:
        cur_message = request.POST['text']
        try:
            room_obj = Room.objects.get(room_name=room_name)
        except Room.DoesNotExist:
            return HttpResponseBadRequest('Invalid room name')
        message = Message(author=request.user,
                          room=room_obj,
                          text=cur_message)
        message.save()
        # one client sends a message; let's broadcast to all clients in the same room
        send_event('room-{}'.format(room_name), 'message', {'message': '{}'.format(message)})

    if request.method == 'POST' or (request.method == 'GET' and not created):
        history_messages = room_obj.room_messages.all().order_by('-time_stamp')[:50]
        history_messages = reversed(history_messages)
    for message in history_messages:
        prev_messages.append('{}'.format(message))
    body = json.dumps(prev_messages, cls=DjangoJSONEncoder) + '\n'
    return HttpResponse(body, content_type='application/json')
