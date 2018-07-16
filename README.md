# Demos to show how pushpin works

## What is fanout/pushpin
[Pushpin](https://pushpin.org/) is an [open-source](https://github.com/fanout) self-hosted realtime push server.

## What is realtime push
>
     The realtime push is a simple protocol using HTTP version 2 to   deliver real time events which can be delivered (or “pushed”) in a   timely fashion. An example would be Slack.  
     In Slack, users can subscribe to channels. If messages are published  
     to a channel(or some channels), all users subscribed to that channel  
     are notified. This procedure is formally called "pub/sub model".
     In a pub/sub model, any message published to a topic is immediately   received by all of the subscribers to the topic.

## What is special with pushpin?
- It is open source(yay!)
- It is self-hosted
    - Pros: User controls everything.
    - Cons: Setting up servers might be tedious. Maintenance cost is high.
    - The "cloud" version of pushpin is fanout(which costs money of course).
- It is more a proxy than a server. More specifically:
    - It is transparent with clients(i.e. clients can be totally unaware of the existence of pushpin server).
    - The backend must handle proxied requests, which means the backend is responsible for subscribing the clients to specific channels.
    - The backend must tell Pushpin to push data. Regardless of how clients are connected, data may be pushed to them by making an HTTP POST request to Pushpin’s private control API (http://localhost:5561/publish/ by default). Pushpin will inject this data into any client connections as necessary.

## Similar products
There are many similar products.

To name a few:
- Pusher(most user-friendly but expensive)
- Pubnub
- Pushwoosh
- ...
