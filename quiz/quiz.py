from random import choice

from django.db.models import Q, F
from wikidata.client import Client

from quiz.models import QuestionType, Object
from game.game import Game
from game.models import Question


class Quiz:
    def __init__(self, game_id):
        self.game = Game.get_game(game_id)
        self.question_types = QuestionType.objects.filter(
            category=self.game.category)
        self.client = Client()

    @classmethod
    def parse_answers(cls, obj):
        return [answer.lower() for answer in obj.right_answers]

    @classmethod
    def get_answers(cls, room_id=None, question_id=None, question=None):
        if not any([room_id, question_id, question]):
            raise ValueError('Room ID or Question ID is required')

        if question:
            return cls.parse_answers(question)
        elif room_id:
            obj = Question.objects.filter(room_id=room_id).order_by('-ask_date')
        else:
            obj = Question.objects.filter(id=question_id)
        if obj.exists:
            obj = obj.first()
            return cls.parse_answers(obj)

    def get_random_type(self):
        return choice(self.question_types)

    def get_random_object(self):
        queryset = Object.objects.filter((
            Q(category_id=self.game.category.id) &
            ~Q(name=F('wikidata_id'))
        ))
        if queryset.exists():
            return choice(queryset)

    @staticmethod
    def get_aliases(obj):
        return list(obj.aliases.all().values_list('name', flat=True))

    def get_answer_list(self, obj):
        answers = self.get_aliases(obj)
        answers.insert(0, obj.name)
        question = Question.objects.create(
            game=self.game.game_db_obj,
            right_answers=answers
        )
        return answers, question.id

    def get_image_url_from_object(self, obj, question_type):
        prop = self.client.get(question_type.question_wikidata_prop)
        wikidata_obj = self.client.get(obj.wikidata_id)
        img = wikidata_obj.get(prop)
        image_url = img.image_url if img else None
        return image_url

    def ask_image_type(self):
        question_type = self.get_random_type()
        obj = self.get_random_object()
        if not obj:
            return None
        image_url = self.get_image_url_from_object(obj, question_type)
        answer_list, question_id = self.get_answer_list(obj)
        return image_url, answer_list, question_id, question_type.text
