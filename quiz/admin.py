from django.contrib import admin
from .models import Question, QuestionType, Object, ObjectAlias, Category, Answer


admin.site.register(
    [Question, QuestionType, Object, ObjectAlias, Category, Answer]
)
