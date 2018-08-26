## Implement Pushpin dashboard

- Read pushpin status from socket provided by pushpin
- Use celery to execute the reading task asynchronously
- Use websocket to send pushpin status in real time
- Integrate channels 2 in order to use websocket in Django