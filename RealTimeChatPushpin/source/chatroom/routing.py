from channels.routing import ProtocolTypeRouter, URLRouter
import chatapp.routing


application = ProtocolTypeRouter({
    # 'http': URLRouter(chatapp.routing.urlpatterns),
})
