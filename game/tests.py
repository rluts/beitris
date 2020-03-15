from django.test import TestCase

from common.exceptions import RoomPermissionsDenied
from game.factories import CategoryFactory, UserFactory, RoomFactory
from game.game import Game
from game.models import GameTable


class TestGame(TestCase):
    def setUp(self) -> None:
        self.category = CategoryFactory()
        self.user = UserFactory()
        self.another_user = UserFactory()
        self.room = RoomFactory()
        self.private_room = RoomFactory(private=True)
        self.game = Game(
            category_id=self.category.id,
            initiator=self.user,
            room=self.room)

    def test_game_creation(self):
        Game(
            category_id=self.category.id,
            initiator=self.user.external_id,
            room=self.room)
        self.assertEqual(GameTable.objects.count(), 2)

    def room_permissions_denied(self):
        with self.assertRaises(RoomPermissionsDenied):
            Game(category_id=self.category.id, initiator=self.user,
                 room=self.private_room)

    def test_join_and_list(self):
        Game.join_room(
            self.user, self.private_room, self.private_room.invide_code)
        my_game = Game(
            category_id=self.category.id,
            initiator=self.user,
            room=self.private_room)
        another_game = Game(
            category_id=self.category.id,
            initiator=self.another_user,
            room=self.private_room)
        list_of_games = Game.list_of_games(self.user)
        self.assertIn(my_game, list_of_games)
        self.assertNotIn(another_game, list_of_games)


