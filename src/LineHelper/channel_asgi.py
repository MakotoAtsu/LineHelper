from channels.routing import ProtocolTypeRouter,URLRouter
from LineHelper import urls

application = ProtocolTypeRouter({
    "websocket":URLRouter(urls.ws_url)
})
