from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from game.ws.consumers import GameCostumer
from game.ws.auth import TokenAuthMiddleware

application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddleware(
        URLRouter([
            path("game/", GameCostumer),
        ]),
    ),
})
