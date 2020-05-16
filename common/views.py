from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.serializers import UserSerializer


@api_view(['GET'])
@ensure_csrf_cookie
def status(request):
    if request.user.is_anonymous:
        return Response({'authorized': False, 'user': None})
    serializer = UserSerializer(request.user)
    return Response({'authorized': True, 'user': serializer.data})
