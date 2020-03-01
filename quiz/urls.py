from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AnswerViewSet, AskView, CategoriesView


router = DefaultRouter()

router.register('answer', AnswerViewSet, basename='answer')

urlpatterns = router.urls + [
    path('ask/', AskView.as_view(), name='ask'),
    path('categories/', CategoriesView.as_view(), name='categories')
]