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

That socket is a ZMQ socket and we can use Python code to do the query.
