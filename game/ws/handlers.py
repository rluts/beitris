from channels.db import database_sync_to_async

from common.converters.images import Image
from common.exceptions import FileTypeError, NotFoundError, BeitrisError
from game.game import Game
from game.ws.serializers import WSGameSerializer, WSCategorySerializer, WSUserSerializer
from quiz.models import Category
from quiz.quiz import Quiz


class GameDBHandler:
    """
    Database handler methods
    """
    def __init__(self, *args, **kwargs):
        self.game = None
        self.scope = {}
        super().__init__(*args, **kwargs)

    @database_sync_to_async
    def handle_get_categories(self):
        queryset = Category.objects.filter(enabled=True)
        serializer = WSCategorySerializer(queryset)
        return serializer.data

    @database_sync_to_async
    def handle_get_and_join_game(self, game):
        game = Game.get_game(game)
        game.join(self.scope['user'])
        return game

    @database_sync_to_async
    def handle_create_game(self, room, category_id):
        game = Game(self.scope['user'], category_id, room)
        serializer = WSGameSerializer(game.game_db_obj)
        return serializer.data

    @database_sync_to_async
    def handle_list_of_games(self):
        games = Game.list_of_games(self.scope['user'])
        serializer = WSGameSerializer(games, many=True)
        return serializer.data

    @database_sync_to_async
    def handle_ask(self):
        quiz = Quiz(self.game.game_db_obj.id)
        response = quiz.ask_image_type()
        if not response:
            return
        img, answers, question_id, question = response
        try:
            image = Image(
                img,
                self.game.room.id,
                question_id,
                convert_svg=False)
            image = str(image).split('/')[-1]
            return {'response': {
                'url': f'/media/{image}',
                'question_id': question_id,
                'question': question
            }}
        except BeitrisError as e:
            return {'error': e.msg, 'code': e.code}
        except AttributeError:
            return {'error': 'Image not found', 'code': 404}

    @database_sync_to_async
    def handle_user_joined(self, user):
        user = WSUserSerializer(user).data
        game = WSGameSerializer(self.game.game_db_obj).data
        data = {'event': 'user_joined', 'user': user, 'game': game}
        return data