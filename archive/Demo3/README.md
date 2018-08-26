# Demo for "Broadcast" push

This demo uses Django as the backend server, Pushpin as the proxy and there clients as the mock frontend.  
Of the three clients two are receiving ones and one is broadcast.


Launch Django server:
```sh
python manage.py runserver 9000
```

Start Pushpin:(note the 'over_http' config meaning that websocket over HTTP is used)
```sh
pushpin --route="* localhost:9000,over_http"
```

Then start the three clients and see the broadcasting.
