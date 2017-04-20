from __future__ import absolute_import, unicode_literals

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .tasks import bot, crawler


class BotViewSet(ViewSet):
    def create(self, request):
        bot_name = request.data.get('name', None)
        if bot_name:
            bot.delay(bot_name)
            return Response({'created': True})
        else:
            return Response({'created': False})


class CrawlerViewSet(ViewSet):
    def create(self, request):
        crawler_name = request.data.get('name', None)
        if crawler_name:
            crawler.delay(crawler_name)
            return Response({'created': True})
        else:
            return Response({'created': False})
