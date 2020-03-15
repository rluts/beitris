import asyncio
import logging

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

from common.enums import MessageTypes
from game.ws.handlers import GameDBHandler
from game.ws.helpers import GameHelper
from game.ws.serializers import WSUserSerializer

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class GameCostumer(AsyncJsonWebsocketConsumer, GameDBHandler, GameHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_in_game = False
        self.game = None
        self.game_group_name = None
        self.quiz = None
        self.current_timer_task = None
        self.full_name = None

    async def connect(self):
        self.scope['user'] = await self.scope['user']
        if self.scope['user'].is_anonymous:
            logger.debug("user anon")
            await self.close(code=403)
        else:
            logger.debug("user %s accepted" % self.scope['user'].username)
            await self.accept()
            self.full_name = WSUserSerializer.get_full_name(self.scope['user'])

    async def receive_json(self, content, **kwargs):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        if not isinstance(content, dict):
            return
        command = content.get('command')
        params = content.get('params', {})
        if command == 'start_game':
            await self.start_game()
        elif command == 'create_game':
            await self.create_game(params.get('category'))
        elif command == 'games_list':
            await self.get_games()
        elif command == 'categories_list':
            await self.get_categories()
        elif command == 'join_game':
            await self.join_game(params.get('game'))
        elif command == 'check_answer':
            pass
        elif command == 'skip':
            await self.request_for_skip()
        elif command == 'message':
            await self.chat_message(params.get('message'))

    async def request_for_skip(self):
        if self.quiz:
            response = await self.handle_request_for_skip(self.scope['user'])
            participants = response['participants']
            skip_requests = response['skip_requests']
            if participants - skip_requests == 0:
                msg = 'Question skipped, loading next quiz.'
                await self.warning_message(msg)
                await self.cancel_timer()
                await self.next_quiz()
            else:
                msg = (f'{self.full_name}: pass. {skip_requests}/{participants}'
                       f' want to skip this question.')
                await self.warning_message(msg)

    async def disconnect(self, code):
        await self.leave_game()

    async def next_quiz(self):
        answer = await self.handle_get_answer()
        msg = f'Right answer: {answer}'
        await self.info_message(msg)
        await self.start_quiz()

    async def info_message(self, message):
        await self.send_game_message(
            message=message,
            message_type=MessageTypes.info.value)

    async def warning_message(self, message):
        await self.send_game_message(
            message=message,
            message_type=MessageTypes.warning.value)

    async def chat_message(self, message):
        await self.send_game_message(
            message=message,
            message_type=MessageTypes.info.value,
            sign=self.scope['user'])

    async def start_game(self):
        if self.game:
            await self.handle_start_game()
            await self.send_game_event('game_started')
            await self.start_quiz()

    async def quiz_timer(self):
        for i in range(20):
            await asyncio.sleep(1)
            await self.send_game_event({'time': 20 - i})
            # TODO: check threads
        await self.next_quiz()

    async def cancel_timer(self):
        if self.current_timer_task and not self.current_timer_task.cancelled():
            self.current_timer_task.cancel()

    async def start_quiz(self):
        if self.game and not self.game.game_db_obj.finished:
            response = await self.handle_ask()
            if response.get('error'):
                logger.error(f'Error {response["code"]}: {response["error"]}')
                return await self.start_quiz()
            await self.send_game_event(response)
            loop = asyncio.get_event_loop()
            self.current_timer_task = loop.create_task(self.quiz_timer())
            self.current_timer_task.get_name()
        else:
            await self.send_json({'response': 'game_finished'})

    async def get_games(self):
        games = await self.handle_list_of_games()
        await self.send_json(games)

    async def get_categories(self):
        categories = await self.handle_get_categories()
        await self.send_json(categories)

    async def create_game(self, category):
        game = await self.handle_create_game(settings.COMMON_ROOM_ID, category)
        await self.send_json(game)

    async def send_game_event(self, content):
        if self.game_group_name:
            await self.channel_layer.group_send(self.game_group_name, {
                "type": 'game.event',
                "content": content,
            })

    async def send_game_message(self, message, message_type, sign=None):
        if message_type not in MessageTypes.values():
            raise ValueError(f'Invalid message type: {message_type}')
        if self.game_group_name and message:
            await self.channel_layer.group_send(self.game_group_name, {
                "type": 'game.message',
                "message_type": message_type,
                "message": message,
                "sign": sign
            })

    async def join_to_game_group(self):
        self.game_group_name = f'game{self.game.game_db_obj.id}'
        await self.channel_layer.group_add(self.game_group_name,
                                           self.channel_name)

    async def join_game(self, game):
        await self.leave_game()
        self.is_in_game = True
        self.game = await self.handle_get_and_join_game(
            game, self.scope['user'])
        await self.join_to_game_group()
        message = f"{self.full_name} joined the game"
        await self.info_message(message)

    async def leave_game(self):
        await self.handle_leave_game(self.scope['user'])
        await self.info_message(f"{self.full_name} left the game")
        self.is_in_game = False
        self.game = None
        self.game_group_name = None
        self.channel_layer.flush()
