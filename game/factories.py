from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory

from game.models import Room
from quiz.models import Category


# TODO: move factories to apps

class UserFactory(DjangoModelFactory):
    username = Faker('user_name')
    email = Faker('email')
    external_id = Faker('random_int')
    default_language = Faker('language_code')

    class Meta:
        model = get_user_model()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room
