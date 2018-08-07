# Demo for pushpin subscription/publish in Django

## Architecture

```  
               +---------------------+                
               |     Django          |                
      +-------->+------------------+ <----------+     
      |        ||                  | |          |     
      |        ||   Event Stream   | |          |     
      | +-------    (Server)       | --------+  |     
      | |      ||------------------| |       |  |     
+-----|-v--+   ||   Django-Grip    | |       |  |     
|          |   ||                  | |    +--v--|----+
| Client 1 |   ++---------^--------+-+    |          |
|          |              |   |           | Client 2 |
+----------+              |   |           |          |
                          |   v           +----------+
                    +------------+                  
                    |            |                  
                    |   Pushpin  |                  
                    +------------+                  
```

We use HTTP Stream with Server Sent Event(SSE) to implement subscribe/publish.  
Django is the backend server.  
Pushpin is the proxy.  
EventStream and Django-Grip is library for pushpin service to be integrated with
Django.  

## Subscribe
Client sends
```HTML
HTTP GET /events/?channel=room-room7
```

Django receives the HTTP request and the corresponding URL dispatcher is:  
```python
re_path(r'^events/', include(django_eventstream.urls)),
```

```python
django_eventstream.urls
```
is Pushpin EventStream library code, which means the library will take care of the subscribe work.



## Publish
