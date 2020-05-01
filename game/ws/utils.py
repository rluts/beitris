from django.contrib.auth import get_user_model
from game.models import GameTable

User = get_user_model()


def ws_restart_cleanup():
    User.objects.all().update(current_channel='', is_online=False)
    GameTable.objects.all().update(finished=True)
