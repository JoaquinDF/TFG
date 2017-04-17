from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .tasks import bot


class BotViewSet(ViewSet):

    def create(self, request):
        bot_name = request.data.get('bot_name', None)
        if bot_name:
            bot.delay(bot_name)
            return Response({'created': True})
        else:
            return Response({'created': False})
