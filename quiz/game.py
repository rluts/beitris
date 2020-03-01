from datetime import datetime, timedelta

from common.exceptions import BackendDoesNotExist
from quiz.models import Game as GameModel, Category, User
from common.enums import Backends


class Game:

    def __init__(self, initiator, category_id, room_id, backend,
                 game_db_obj=None):
        if backend not in Backends.values():
            raise BackendDoesNotExist
        self.category = Category.objects.get(id=category_id)
        self.participant = None
        self.backend = backend
        self.started = False
        self.started_time = None
        self.initiator = self.get_or_create_user(initiator)
        self.game_db_obj = game_db_obj or (
            GameModel.objects.create(
                category_id=category_id,
                backend=backend,
                room_id=room_id,
                initiator_id=self.initiator.id
            )
        )

    @classmethod
    def get_game(cls, room_id, category_id):
        game_db_obj = GameModel.objects.filter(
            room_id=room_id,
            category_id=category_id,
            created_time__lt=datetime.now() - timedelta(hours=1),
            finished=False
        )
        if game_db_obj.exists():
            game_db_obj = game_db_obj.first()
            return cls(game_db_obj.initiator_id, game_db_obj.category_id,
                       game_db_obj.room_id, game_db_obj.backend, game_db_obj)

    def get_or_create_user(self, external_id):
        user, created = User.objects.get_or_create(username=external_id,
                                                   external_id=external_id,
                                                   backend=self.backend)

        return user

    def join(self, participant):
        self.game_db_obj.participant = self.get_or_create_user(participant)
        self.start_game()
        self.game_db_obj.save()

    def _setattr(self, key, value):
        setattr(self, key, value)
        setattr(self.game_db_obj, key, value)

    def start_game(self):
        self._setattr('started', True)
        self._setattr('start_time', datetime.now())

    def finish_game(self):
        self._setattr('finished', True)
        self._setattr('end_time', datetime.now())

    def is_multiple_game(self):
        return bool(self.participant)

