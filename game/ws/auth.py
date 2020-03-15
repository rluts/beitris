import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    @database_sync_to_async
    def get_user(self, token):
        token_lookup = None
        try:
            token_lookup = Token.objects.get(key__in=token)
        except Token.DoesNotExist:
            pass
        return token_lookup.user if token_lookup else AnonymousUser()

    def __call__(self, scope):
        query = parse_qs(scope['query_string'].decode())
        scope['user'] = self.get_user(query.get('token', []))
        return self.inner(scope)

