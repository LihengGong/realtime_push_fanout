# Demo1: use pushpin as the proxy, Django as the backend, and curl as the front end.

## How to run.
- Make sure [pushpin](https://pushpin.org/docs/install/) is correctly installed.

- In source code root directory:
```sh
pip install django-grip
```

1. Run **without** pushpin.

```
+------------------+                 +----------------------+  
|                  +---------------> |                      |  
|                  |                 |                      |  
|     client       |                 |       Django         |  
|                  | <---------------+                      |  
|                  |                 |                      |  
|                  |                 |                      |  
+------------------+                 +----------------------+  
```

- Launch Django server:
```sh
python manage.py startserver
```
- Send data and see the echo:
```sh
curl -i -H 'Content-Type: application/websocket-events' -d OPEN$'\r'$'\n' http://127.0.0.1:8000/users/socket/
```
<br><br>

2. Run **with** pushpin.

```
+-------------------+         +-------+         +-------------------------+
|                   +-------> |       +-------> |                         |
|                   |         |       |         |                         |
|      client       |         |pushpin|         |         Django          |
|                   |         |       |         |                         |
|                   | <-------+       | <-------+                         |
|                   |         |       |         |                         |
|                   |         |       |         |                         |
+-------------------+         +-------+         +-------------------------+
```
- Launch Django server:
```sh
python manage.py startserver
```

- Start pushpin:
```sh
pushpin --route="* localhost:8000"
```

- Send data and see the echo:
```sh
curl -i -H 'Content-Type: application/websocket-events' -d OPEN$'\r'$'\n' http://127.0.0.1:7999/users/socket/
```

And an expected sample output is:
```sh
HTTP/1.1 200 OK
Date: Mon, 16 Jul 2018 20:13:43 GMT
Server: WSGIServer/0.2 CPython/3.6.3
Content-Type: application/websocket-events
Sec-WebSocket-Extensions: grip
X-Frame-Options: SAMEORIGIN
Content-Length: 59

OPEN
TEXT 2a
c:{"channel": "test", "type": "subscribe"}
```

## Resources:
The discussion in [this link](https://github.com/fanout/django-grip/issues/1) is a perfect reference for what happens.
