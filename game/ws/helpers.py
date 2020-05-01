import logging

from channels.db import database_sync_to_async

from common.converters.images import Image
from common.enums import Backends
from common.exceptions import BeitrisError
from game.game import Game
from game.models import Room
from game.ws.serializers import WSUserSerializer, WSCategorySerializer, WSGameSerializer
from quiz.models import Category
from quiz.quiz import Quiz

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class GameHelper:
    def __init__(self, user):
        self.user = user

    @database_sync_to_async
    def get_categories(self):
        queryset = Category.objects.filter(enabled=True)
        serializer = WSCategorySerializer(queryset, many=True)
        return serializer.data

    @database_sync_to_async
    def get_serialized_user(self):
        return WSUserSerializer(self.user).data

    @database_sync_to_async
    def get_and_join_game(self, game, user):
        game = Game.get_game(game)
        game.join(user)
        return game

    @database_sync_to_async
    def leave_game(self, game):
        if self.user in game.game_db_obj.participants.all():
            game.game_db_obj.participants.remove(self.user)
            return True

    @database_sync_to_async
    def create_game(self, category_id):
        # TODO: refactor retrieval the room
        room, _ = Room.objects.get_or_create(backend=Backends.api.value)
        game = Game(self.user, category_id, room)
        serializer = WSGameSerializer(game.game_db_obj)
        return serializer.data, game

    @database_sync_to_async
    def list_of_games(self):
        games = Game.list_of_public_games()
        serializer = WSGameSerializer(games, many=True)
        return serializer.data

    @database_sync_to_async
    def get_quiz(self, game, current_question=None):
        return Quiz(game.game_db_obj.id, current_question=current_question)

    @database_sync_to_async
    def ask(self, game):
        if not game.participants.exists():
            return
        quiz = Quiz(game.game_db_obj.id)
        response = quiz.ask_image_type()
        if not response:
            return
        img, answers, question_id, question = response
        try:
            image = Image(
                img,
                game.room.id,
                question_id,
                convert_svg=False)
            image = str(image).split('/')[-1]
            return quiz, {'response': {
                'url': f'/media/{image}',
                'question_id': question_id,
                'question': question
            }}
        except BeitrisError as e:
            return self.ask(game)
        except AttributeError:
            return self.ask(game)

    @database_sync_to_async
    def start_game(self, game):
        game.start_game()

    @database_sync_to_async
    def is_skipped(self, quiz):
        return quiz.is_skipped()

    @database_sync_to_async
    def request_for_skip(self, quiz):
        return quiz.skip_request(self.user)

    @database_sync_to_async
    def get_answer(self, quiz):
        answer = next(iter(quiz.current_question.right_answers), None)
        quiz.current_question = None
        if not answer:
            raise ValueError('Answers does not exist')
        return answer
