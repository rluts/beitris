from django.contrib.auth import get_user_model
from rest_framework import serializers

from game.models import GameTable
from quiz.models import Category

User = get_user_model()


class WSCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class WSUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(obj):
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ('id', 'full_name', 'is_online')


class WSGameSerializer(serializers.ModelSerializer):
    initiator = WSUserSerializer()
    participants = WSUserSerializer(many=True)
    category = WSCategorySerializer()

    class Meta:
        model = GameTable
        fields = ('id', 'room_id', 'initiator', 'participants', 'category', 'created_time',
                  'started', 'start_time', 'finished')


class ReceivedDataSerializer(serializers.Serializer):
    command = serializers.CharField()
    params = serializers.JSONField(required=False)
