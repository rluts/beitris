from django.http.response import Http404
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.converters.images import Image
from common.exceptions import FileTypeError, NotFoundError
from game.game import Game
from game.models import Answer, Room
from quiz.models import Category
from quiz.quiz import Quiz
from quiz.serializers import CategorySerializer, AnswerSerializer


ANONYMOUS_USER_ID = 2
SPA_ROOM_ID = 1
BACKEND = 'api'


class CategoriesView(ListAPIView):
    queryset = Category.objects.filter(enabled=True)
    serializer_class = CategorySerializer


class AskView(CreateAPIView):
    """
    Quick refactor from flask to DRF;
    Need to rework
    """
    def post(self, request, *args, **kwargs):
        category_id = request.data.get('category')
        if not category_id:
            raise Http404
        room, _ = Room.objects.get_or_create(id=SPA_ROOM_ID)
        game = Game(ANONYMOUS_USER_ID, category_id, room)
        quiz = Quiz(game_id=game.game_db_obj.id)
        response = quiz.ask_image_type()
        if not response:
            return Response({'error': 'Not configured'})
        img, answers, question_id, question = response

        try:
            image = Image(img, game.room.id, question_id, convert_svg=False)
            image = str(image).split('/')[-1]
            return Response({
                'url': f'/media/{image}',
                'question_id': question_id,
                'question': question
            })
        except (FileTypeError, NotFoundError) as e:
            return Response({'error': e.msg}, status=e.code)
        except AttributeError:
            return Response({'error': 'Image not found'}, status=404)


class AnswerViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = AnswerSerializer
    model = Answer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = serializer.validated_data['answer']
        question = serializer.validated_data['question']
        if Answer.objects.filter(question=question).exists():
            return Response({'result': 'Already answered'}, status=400)
        if result.lower().strip() in Quiz.get_answers(question=question):
            serializer.validated_data['right'] = True
            serializer.validated_data.pop('answer')
            self.perform_create(serializer)
            return Response({'result': 'OK'})
        else:
            return Response({'result': 'FAIL'})

    @action(methods=['post'], url_path='get_answer', detail=False)
    def get_answer(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.validated_data['question']
        self.perform_create(serializer)
        return Response({'result': question.right_answers})

