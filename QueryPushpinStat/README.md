# Query Pushpin's stats

In Pushpin's [RUN] directory, there are several socket files.  
Only one of them, `pushpin-stats`, is documented.

## Why do we need to query Pushpin's status

We would like to know the status of Pushpin. To name a few:
- How many connections(clients) does Pushpin have now?
- How many subscribers are there?
- What is the peer's IP address?
- ...

## How to query?

As stated above, there are several socket files created by Pushpin in
its [RUN] directory. This [RUN] directory can be configured in  
/usr/local/etc/pushpin/pushpin.conf.  
For example, it can be configured as: /usr/local/var/run/pushpin  

That socket is a [ZMQ socket](https://github.com/zeromq/pyzmq) and we can use Python code to do the query.  
The Python code is quite simple and straightforward.

First, connect to the socket.
```python
  sock_file = #[dir of Pushpin's run directory]
  ctx = zmq.Context()
  sock = ctx.socket(zmq.SUB)
  sock.connect(sock_file)
  sock.setsockopt(zmq.SUBSCRIBE, b"")
```

Then receive data:
```python
  # note that in Python3, the data received from the socket is raw binary. That's why there is the 'b' prefix.
  while True:
    m_raw = sock.recv()
    mtype, mdata = m_raw.split(b' ', 1)
    if len(mdata) > 1:
      process_data(mtype, mdata)
```

## Several problems to consider

1. How to send the Pushpin stat data to frontend?

2. How to keep record the Pushpin stat data?

3. Should the socket reading method be placed in Django view method?
