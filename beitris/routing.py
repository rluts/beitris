from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from game.ws.consumers import GameConsumer
from game.ws.auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddlewareStack(
        URLRouter([
            path("game/", GameConsumer),
        ]),
    ),
})
