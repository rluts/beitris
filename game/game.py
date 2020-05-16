from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Q

from common.exceptions import RoomPermissionsDenied, RoomNotFound
from game.models import GameTable, Room
from quiz.models import Category

User = get_user_model()


class Game:

    def __init__(self, initiator, category_id, room,
                 game_db_obj=None):
        self.category = Category.objects.get(id=category_id)
        self.started = False
        self.started_time = None
        if not isinstance(room, Room):
            room = Room.objects.get(id=room)
        self.room = room
        initiator = self.get_or_create_user(initiator)

        if (self.room.private and self.room.creator != initiator and
                initiator not in self.room.participants.all()):
            raise RoomPermissionsDenied
        self.game_db_obj = game_db_obj or (
            GameTable.objects.create(
                category_id=category_id,
                room=room,
                initiator=initiator
            )
        )
        self.join(initiator)

    @property
    def participants(self):
        return self.game_db_obj.participants.all()

    @classmethod
    def list_of_games(cls, user):
        game_filter = ((Q(room__creator=user) | Q(room__participants=user)) &
                       Q(finished=False))
        games = GameTable.objects.filter(game_filter)

    @classmethod
    def list_of_public_games(cls):
        # TODO: add language support
        GameTable.objects.filter(finished=False, participants__is_online=None).update(finished=True)
        return GameTable.objects.filter(finished=False)

    def join(self, user):
        self.game_db_obj.participants.add(user)

    @classmethod
    def get_game(cls, game_id):
        game_db_obj = GameTable.objects.get(id=game_id)
        return cls(game_db_obj.initiator, game_db_obj.category_id,
                   game_db_obj.room_id, game_db_obj)

    def get_or_create_user(self, user_obj):
        """
        Get user object
        :param user_obj: user or external_id
        :return:
        """
        if isinstance(user_obj, User):
            return user_obj

        user, created = User.objects.get_or_create(username=user_obj)

        return user

    @classmethod
    def join_room(cls, user, room_id, invite_code=None):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise RoomNotFound
        if room.invite_code == invite_code or not room.private:
            room.participants.add(user)
            return True

    def _setattr(self, key, value):
        setattr(self, key, value)
        setattr(self.game_db_obj, key, value)
        self.game_db_obj.save()

    def start_game(self):
        self._setattr('started', True)
        self._setattr('start_time', datetime.now())

    def finish_game(self):
        self._setattr('finished', True)
        self._setattr('end_time', datetime.now())
