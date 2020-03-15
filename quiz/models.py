from django.contrib.auth import get_user_model
from django.db import models

from common.enums import QuestionTypes
from game.models import GameTable

User = get_user_model()


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
    language = models.CharField(max_length=3, default='en')

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


class QuestionType(models.Model):
    class Meta:
        verbose_name_plural = 'Question Types'
    text = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    question_wikidata_prop = models.CharField(max_length=35)
    type = models.CharField(choices=QuestionTypes.to_choices(), max_length=10)
    is_question_in_child = models.BooleanField(default=False)
    child_prop = models.CharField(null=True, blank=True, max_length=35)

    def __str__(self):
        return self.text
