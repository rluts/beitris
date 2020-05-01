import asyncio
import logging

from game.ws.base_consumer import BaseConsumer, command
from game.ws.exceptions import GameNotJoined
from game.ws.helpers import GameHelper

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class GameConsumer(BaseConsumer):
    helper_class = GameHelper
    game = None
    current_quiz = None
    QUIZ_TIMER_SECONDS = 30

    async def connect(self):
        await super(GameConsumer, self).connect()
        if not self.scope['user'].is_anonymous and self.scope['user'].is_active:
            await self.post_connect()

    async def post_connect(self):
        await self.response_message('user_info', await self.helpers.get_serialized_user())
        await self.games_list()

    @command
    async def message(self, data):
        if message := data.get('message'):
            await self.send_group_message(self.game_id, 'message', {'message': message})

    @command
    async def create_game(self, data):
        if category := data.get('category'):
            data, self.game = await self.helpers.create_game(category)
            await self.channel_layer.group_add(self.game_id, self.channel_name)
            await self.response_message(data)
            await self.channel_layer.group_add(f'game{self.game.game_db_obj.id}', self.channel_name)

    @property
    def game_id(self):
        return f'game{self.game.game_db_obj.id}'

    @command
    async def join_game(self, data):
        game_id = data.get('game')
        if game_id and isinstance(game_id, int):
            self.game = await self.helpers.get_and_join_game(game_id, self.scope['user'])
            self.current_quiz = await self.helpers.get_quiz(self.game)
            await self.response_message(
                'question', await self.helpers.get_response(self.current_quiz))
            await self.channel_layer.group_add(self.game_id, self.channel_name)
            await self.send_group_message(self.game_id, 'user_joined',
                                          await self.helpers.get_serialized_user())

    @command
    async def skip(self):
        if self.current_quiz:
            details = await self.helpers.request_for_skip(self.current_quiz)
            await self.send_group_message(self.game_id, 'request_for_skip',
                                          {'user': await self.helpers.get_serialized_user(),
                                           'details': details})

    @command
    async def categories_list(self):
        data = await self.helpers.get_categories()
        await self.response_message('categories_list', data)

    @command
    async def games_list(self):
        await self.response_message('games_list', await self.helpers.list_of_games())

    @command
    async def check_answer(self, data):
        if answer := data.get('answer'):
            await self.send_group_message(self.game_id, 'answer',
                                          await self.helpers.get_serialized_user())
            is_right = await self.helpers.check_answer(self.current_quiz, answer)
            if not is_right:
                await self.send_group_message(self.game_id, 'answer_wrong',
                                              {'user': await self.helpers.get_serialized_user(),
                                               'answer': answer})

    @command
    async def start_game(self):
        if not self.game:
            raise GameNotJoined
        await self.helpers.start_game(self.game)
        if not hasattr(self.channel_name, 'task'):
            self.channel_layer.task = {}
        self.channel_layer.task[f'game{self.game.game_db_obj.id}'] = asyncio.create_task(
            self.timer())

    async def get_answer(self):
        answer = await self.helpers.get_answer(self.current_quiz)
        await self.send_group_message(f'game{self.game.game_db_obj.id}', 'answer', answer)
        self.current_quiz = None

    async def timer(self):
        await self.ask()
        for i in reversed(range(self.QUIZ_TIMER_SECONDS)):
            if await self.helpers.is_skipped(self.current_quiz):
                await self.send_group_message(self.game_id, 'question_skipped')
                break
            if response := await self.helpers.is_answered(self.current_quiz):
                user, right_answer = response
                user = await self.helpers.get_serialized_user(user=user)
                await self.send_group_message(self.game_id, 'answer_correct', user)
                break
            await self.send_group_message(self.game_id, 'timer', {'time': i})
            await asyncio.sleep(1)
        await self.get_answer()
        await self.timer()

    async def ask(self):
        await self.send_group_message(self.game_id, 'loading_quiz')
        result = await self.helpers.ask(self.game)
        if result is None:
            return
        self.current_quiz, data = result
        await self.channel_layer.group_send(
            self.game_id,
            {"type": "set_quiz_handler"},
        )
        await self.send_group_message(f'game{self.game.game_db_obj.id}', 'question', data)

    async def set_quiz_handler(self, event):
        self.current_quiz = await self.helpers.get_quiz(self.game)

    async def disconnect(self, code):
        if self.game:
            await self.helpers.leave_game(self.game)
            await self.channel_layer.group_discard(self.game_id, self.channel_name)
            await self.send_group_message(self.game_id, 'disconnected',
                                          await self.helpers.get_serialized_user())
        await super().disconnect(code)
