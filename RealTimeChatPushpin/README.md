## Real-time chat using Pushpin as push service, with user registration and authentication

### System setup
SSE(Server Sent Event) is used for server push. Fanout/eventstream is a handy library for SSE for Django.  
Channels library is used for its event-driven functionality. Actually, Fanout/eventstream is dependent on Channels library.
Pushpin is used for publish/subscribe.
Vue.js is used as frontend.


### TODO
- Restructure code
- Improve frontend code structure(Vue.js)


### Pushpin log

From pushpin log, subscribe and publish work as expected.  
```
[INFO] 2018-09-01 09:54:58.162 [handler] subscribe http://localhost:7999/events/?channel=room-default channel=events-room-default

[INFO] 2018-09-01 09:54:58.162 [handler] subscribe http://localhost:7999/events/?channel=room-default channel=user-2

[INFO] 2018-09-01 09:55:04.457 [handler] publish channel=events-room-default receivers=1
```

