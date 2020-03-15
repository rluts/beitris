from abc import abstractmethod

from game.ws.serializers import WSUserSerializer


class GameHelper:
    @abstractmethod
    def send_json(self, param):
        pass

    async def game_event(self, event):
        await self.send_json({'response': event['content']})

    async def game_message(self, event):
        value = {
            'message_type': event['message_type'],
            'message': event['message']
        }
        if event['sign']:
            value['sign'] = WSUserSerializer(event['sign'])
        await self.send_json(value)
