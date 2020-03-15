from rest_framework import serializers

from quiz.models import Category
from game.models import Answer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class AnswerSerializer(serializers.ModelSerializer):

    answer = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Answer
        fields = ('answer', 'question')
