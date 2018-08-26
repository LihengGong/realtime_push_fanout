from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import dashboard.routing


application = ProtocolTypeRouter({
    # Http->Django views is added by default
    'websocket': AuthMiddlewareStack(
        URLRouter(
            dashboard.routing.websocket_urlpatterns
        )
    ),
})
