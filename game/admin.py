from django.contrib import admin
from game.models import GameTable, Room, Answer, Question

admin.site.register([GameTable, Room, Answer, Question])
