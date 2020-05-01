from django.apps import AppConfig


class GameConfig(AppConfig):
    name = 'game'

    def ready(self):
        from game.ws.utils import ws_restart_cleanup
        ws_restart_cleanup()
