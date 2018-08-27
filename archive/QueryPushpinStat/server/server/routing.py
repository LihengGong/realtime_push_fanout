from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import testWhile.routing


application = ProtocolTypeRouter({
    # Http->Django views is added by default
    'websocket': AuthMiddlewareStack(
        URLRouter(
            testWhile.routing.websocket_urlpatterns
        )
    ),
})
