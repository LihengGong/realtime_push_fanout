## Implement Pushpin dashboard

- Read pushpin status from socket provided by pushpin
- Use celery to execute the reading task asynchronously
- RabbitMQ is used as the broker of celery
- Use websocket to send pushpin status in real time
- Use Redis as the transport
- Integrate channels 2 in order to use websocket in Django
- Use PostgreSQL


### TODO
Improve backend code structure
Implement frontend