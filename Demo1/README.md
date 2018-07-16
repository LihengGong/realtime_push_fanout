Django-LiveResource
-------------------
Author: Justin Karneges <justin@fanout.io>

LiveResource library for Python/Django.

Requirements
------------

* django-grip

Install
-------

You can install from PyPi:

    sudo pip install django-liveresource

Or from this repository:

    sudo python setup.py install

Sample usage
------------

Set GRIP_PROXIES in settings.py:

```python
# pushpin and/or fanout.io is used for sending realtime data to clients
GRIP_PROXIES = [
    # pushpin
    {
        'key': 'changeme',
        'control_uri': 'http://localhost:5561'
    }
    # fanout.io
    #{
    #    'key': b64decode('your-realm-key'),
    #    'control_uri': 'http://api.fanout.io/realm/your-realm',
    #    'control_iss': 'your-realm'
    #}
]
```

You can also set any other EPCP servers that aren't necessarily proxies with PUBLISH_SERVERS:

```python
PUBLISH_SERVERS = [
    {
        'uri': 'http://example.com/base-uri',
        'iss': 'your-iss',
        'key': 'your-key'
    }
]
```

Include GripMiddleware and LiveResourceMiddleware, in that order:

```python
MIDDLEWARE_CLASSES = (
    ...
    'django_grip.GripMiddleware',
    'django_liveresource.LiveResourceMiddleware',
    ...
)
```
