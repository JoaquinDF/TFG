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
        with Mongodb() as mongodb:
            db = mongodb.db
            collection = request.query_params.get('collection', None)
            if collection and collection in db.collection_names():
                response = {}
                coll = db[collection]
                page = request.query_params.get('page', None)
                if not page:
                    url = request.build_absolute_uri(request.path_info
                                                     + '?collection=' + collection
                                                     + '&page=0')
                    return HttpResponseRedirect(url)
                try:
                    p = int(page)
                except ValueError:
                    return HttpResponseBadRequest()
                skip = p * 10
                limit = 10
                results = json.loads(dumps(coll.find({}, skip=skip, limit=limit)))
                count = len(results)
                nxt = None
                prv = None
                if count == limit:
                    nxt = request.build_absolute_uri(request.path_info
                                                     + '?collection=' + collection
                                                     + '&page=' + str(p + 1))
                if p > 0:
                    prv = request.build_absolute_uri(request.path_info
                                                     + '?collection=' + collection
                                                     + '&page=' + str(p - 1))
                response['count'] = coll.count({})
                response['next'] = nxt
                response['previous'] = prv
                response['results'] = results

            else:
                response = db.collection_names()
        return Response(response)
