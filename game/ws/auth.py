import logging
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


@database_sync_to_async
def get_user(token):
    try:
        token_lookup = Token.objects.get(key__in=token)
    except Token.DoesNotExist:
        token_lookup = None
    return token_lookup.user if token_lookup else AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __call__(self, scope):

        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        query = parse_qs(self.scope['query_string'].decode()).get('token', [])
        self.scope['user'] = await get_user(query)
        inner = self.inner(self.scope)
        return await inner(receive, send)


def token_auth_middleware_stack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))


TokenAuthMiddlewareStack = token_auth_middleware_stack
