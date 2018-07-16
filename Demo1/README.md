# fanout/pushpin demos

## Demo1: use pushpin as the proxy, Django as the backend, and curl as the front end.

How to run.
- Make sure [pushpin](https://pushpin.org/docs/install/) is correctly installed.

- In source code root directory:
```sh
pip install django-grip
```

<p>Run **without** pushpin.

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


<p>Run **with** pushpin.

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
