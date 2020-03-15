from django.contrib import admin
from .models import QuestionType, Object, ObjectAlias, Category


admin.site.register(
    [QuestionType, Object, ObjectAlias, Category]
)
