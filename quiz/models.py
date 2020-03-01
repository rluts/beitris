from django.db import models
from django.contrib.postgres.fields import JSONField

from common.models import User


BACKEND_CHOICES = (
    ('api', 'API'),
    ('tg', 'Telegram')
)


class Question(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    room_id = models.BigIntegerField()
    ask_date = models.DateTimeField(auto_now_add=True)
    right_answers = JSONField()
    associated_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                        null=True, blank=True)

    def __str__(self):
        return f'Question #{self.pk} (game {self.game_id})'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)
    right = models.BooleanField(default=False)

    def __str__(self):
        return f'User {self.user} for the question {self.question}'


class Game(models.Model):
    initiator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='created_name')
    participant = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='participants_games')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    room_id = models.BigIntegerField()
    backend = models.CharField(choices=BACKEND_CHOICES, max_length=10)
    created_time = models.DateTimeField(auto_now_add=True)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Game #{self.pk}'


class Object(models.Model):
    class Meta:
        unique_together = (
            ('category', 'wikidata_id'),
            ('category', 'name')
        )
    name = models.CharField(max_length=255)
    wikidata_id = models.CharField(max_length=35)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    wikidata_parent_entity = models.CharField(null=True, blank=True,
                                              max_length=35)
    name = models.CharField(max_length=35)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ObjectAlias(models.Model):
    class Meta:
        verbose_name_plural = 'Object Aliases'
    name = models.CharField(max_length=255)
    object = models.ForeignKey(Object, on_delete=models.CASCADE,
                               related_name='aliases')

    def __str__(self):
        return self.name


QUESTION_TYPE_TYPES = (
    ('image', 'IMAGE'),
    ('text', 'TEXT'),
    ('sound', 'SOUND'),
    ('coords', 'SOUND'),
)


class QuestionType(models.Model):
    class Meta:
        verbose_name_plural = 'Question Types'
    text = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    question_wikidata_prop = models.CharField(max_length=35)
    type = models.CharField(choices=QUESTION_TYPE_TYPES, max_length=10)
    is_question_in_child = models.BooleanField(default=False)
    child_prop = models.CharField(null=True, blank=True, max_length=35)

    def __str__(self):
        return self.text
