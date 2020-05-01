import logging
import re

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer, AcceptConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from common.exceptions import BeitrisError
from .exceptions import ForceDisconnect, WebsocketErrors, UnexpectedCommand, ParamsRequired
from .serializers import ReceivedDataSerializer

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


def command(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    inner._is_command = True
    return inner


class BaseConsumer(AsyncJsonWebsocketConsumer):
    helper_class = None
    helpers = None
    groups = ['users_online']

    def is_accepted(self, method):
        return getattr(getattr(self, method, None), '_is_command', None)

    def get_helper_class(self):
        if not self.helper_class:
            raise NotImplemented('helper_class must set')
        return self.helper_class

    @database_sync_to_async
    def set_channel(self):
        self.scope['user'].current_channel = self.channel_name
        self.scope['user'].is_online = True
        self.scope['user'].save()

    @database_sync_to_async
    def disconnect_user(self):
        if not self.scope['user'].is_anonymous:
            self.scope['user'].current_channel = ''
            self.scope['user'].is_online = False
            self.scope['user'].save()

    @database_sync_to_async
    def check_another_client_connected(self):
        self.scope['user'].refresh_from_db()
        if self.scope['user'].is_online:
            if not self.scope['user'].current_channel:
                return
            else:
                return self.scope['user'].current_channel

    async def warning(self, message):
        await self.send_json({'warning': message})

    async def send_message_to_user(self, channel_name, message, data):
        await self.channel_layer.send(channel_name, {'type': 'user_message',
                                                     'message': message, 'params': data})

    async def send_public_message(self, message, data: dict = None):
        if not data:
            data = {}
        await self.channel_layer.group_send(
            'users_online',
            {"type": "group_message", "data": data, "message": message},
        )

    async def user_message(self, event):
        data = event.get('data')
        message = event.get('message')
        await self.response_message(message, data)

    async def response_message(self, message, data: dict = None):
        if not data:
            data = {}
        await self.send_json({'message': message, 'params': data})

    async def info(self, message):
        await self.send_json({'info': message})

    async def error(self, error: WebsocketErrors):
        error_type, code, message = error.value
        await self.send_json({'error': {'type': error_type, 'message': message, 'code': code}})
        return code

    @staticmethod
    def _underscope(s):
        return '_'.join(map(lambda x: x.lower(), re.findall(r'[A-Z][a-z0-9]*', s)))

    async def error_handler(self, error):
        t = self._underscope(error.__class__.__name__)
        message = error.msg
        code = error.code
        await self.send_json({'error': {'type': t, 'message': message, 'code': code}})

    async def connect(self):
        helper_class = self.get_helper_class()
        if self.scope['user'].is_anonymous:
            logger.debug("User not authorized")
            await self.close(code=401)
        elif not self.scope['user'].is_active:
            await self.close(code=403)
        else:
            logger.debug("User %s accepted" % self.scope['user'].username)
            another_connected_client = await self.check_another_client_connected()
            await self.accept()
            await self.set_channel()
            if not isinstance(getattr(self.channel_layer, 'tasks', None), dict):
                self.channel_layer.tasks = {}
            if another_connected_client:
                await self.warning('Another client is connected. It will be disconnected')
                await self.channel_layer.send(
                    another_connected_client, {'type': 'force_disconnect'})

        self.helpers = helper_class(user=self.scope['user'])

    async def disconnect(self, code):
        await self.disconnect_user()

    async def receive_json(self, content, **kwargs):
        serializer = ReceivedDataSerializer(data=content)
        if serializer.is_valid() and self.is_accepted(serializer.validated_data['command']):
            if serializer.validated_data.get('params'):
                await getattr(self, serializer.validated_data['command'])(
                    serializer.validated_data['params']
                )
            else:
                try:
                    await getattr(self, serializer.validated_data['command'])()
                except TypeError as ex:
                    if "missing 1 required positional argument: 'params'" in ex.args[0]:
                        raise ParamsRequired
                    else:
                        raise ex
        else:
            raise UnexpectedCommand

    async def force_disconnect(self, event):
        raise ForceDisconnect()

    async def check_online(self, event):
        await self.set_channel()

    async def send_group_message(self, group, message, data: dict = None):
        if not data:
            data = {}
        await self.channel_layer.group_send(
            group,
            {"type": "group_message", "data": data, "message": message},
        )

    async def group_message(self, event):
        data = event.get('data')
        message = event.get('message')
        if data and message:
            await self.send_json({'message': message, 'data': data})

    async def dispatch(self, message):
        try:
            await super(BaseConsumer, self).dispatch(message)
        except BeitrisError as ex:
            await self.error_handler(ex)

    async def __call__(self, receive, send):
        try:
            await super().__call__(receive, send)
        except ForceDisconnect:
            code = await self.error(WebsocketErrors.ERROR_3001)
            await self.close(code)
        except Exception as ex:
            await self.disconnect(500)
            raise ex
