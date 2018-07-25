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
