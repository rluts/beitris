import random

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from common.enums import Backends

User = get_user_model()


class Room(models.Model):
    class Meta:
        unique_together = (('backend', 'external_id'), )
    backend = models.CharField(choices=Backends.to_choices(), max_length=10)
    external_id = models.BigIntegerField(null=True, db_index=True)
    language = models.CharField(max_length=3, default='en')
    private = models.BooleanField(default=False)
    creator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='created_rooms')
    participants = models.ManyToManyField(User, related_name='rooms')
    invite_code = models.CharField(max_length=8)

    def get_game(self):
        self.games.filter(finished=False)

    @staticmethod
    def generate_invite_code():
        num = str(random.randint(1, 99999999))
        num_len = 8 - len(num)
        return num if not num_len else '0' * num_len + num

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.invite_code = self.generate_invite_code()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'Room #{self.pk}'


class GameTable(models.Model):
    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        db_table = 'game'

    initiator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='created_name')
    participants = models.ManyToManyField(
        User, related_name='participants_games')
    category = models.ForeignKey('quiz.Category', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
                             related_name='games')
    current_question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=3, default='en')
    max_participant = models.PositiveSmallIntegerField(default=10)
    # channel = models.CharField()

    def start(self):
        self.started = True
        self.start_time = timezone.now()
        self.save()

    def __str__(self):
        return f'Game #{self.pk}'


class Question(models.Model):
    game = models.ForeignKey(GameTable, on_delete=models.CASCADE)
    ask_date = models.DateTimeField(auto_now_add=True)
    right_answers = JSONField()
    associated_user = models.ForeignKey(User, on_delete=models.SET_NULL,
                                        null=True, blank=True)
    skip_request = models.ManyToManyField(User, related_name='skip_question')
    response_json = JSONField(null=True, blank=True)

    def __str__(self):
        return f'Question #{self.pk} (game {self.game_id})'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)
    answer = models.CharField(max_length=255)
    right = models.BooleanField(default=False)

    def __str__(self):
        return f'User {self.user} for the question {self.question}'
