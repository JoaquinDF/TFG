import json

from bson.json_util import dumps
from utils.mongodb import Mongodb
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .tasks import bot_task, crawler_task


class BotViewSet(ViewSet):
    def create(self, request):
        bot_name = request.data.get('name', None)
        if bot_name:
            bot_task.delay(bot_name)
            return Response({'name': bot_name, 'queued': True})
        else:
            return Response({'name': bot_name, 'queued': False})


class CrawlerViewSet(ViewSet):
    def create(self, request):
        crawler_name = request.data.get('name', None)
        if crawler_name:
            crawler_task.delay(crawler_name)
            return Response({'name': crawler_name, 'queued': True})
        else:
            return Response({'name': crawler_name, 'queued': False})


class DataViewSet(ViewSet):
    def list(self, request):
        default = '100'
        with Mongodb() as mongodb:
            db = mongodb.db
            collection = request.query_params.get('collection', None)
            if collection and collection in db.collection_names():
                c = db[collection]
                try:
                    limit = int(request.query_params.get('limit', default))
                    offset = int(request.query_params.get('offset', '0'))
                except ValueError:
                    return HttpResponseBadRequest()
                prv = nxt = None
                l = offset - limit
                if l >= 0:
                    prv = request.build_absolute_uri(request.path_info + '?collection=' + collection + '&limit=' + str(limit) + '&offset=' + str(l))
                l = offset + limit
                if l < c.count():
                    nxt = request.build_absolute_uri(request.path_info + '?collection=' + collection + '&limit=' + str(limit) + '&offset=' + str(l))
                response = dict()
                response['count'] = c.count({})
                response['next'] = nxt
                response['previous'] = prv
                response['results'] = json.loads(dumps((c.find({}, skip=offset, limit=limit))))
            else:
                response = db.collection_names()
        return Response(response)
