from __future__ import absolute_import, unicode_literals

import os
from configparser import ConfigParser
from pymongo import MongoClient
from bson.json_util import dumps

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .tasks import bot_task, crawler_task


class BotViewSet(ViewSet):
    def create(self, request):
        bot_name = request.data.get('name', None)
        if bot_name:
            bot_task.delay(bot_name)
            return Response({'created': True})
        else:
            return Response({'created': False})


class CrawlerViewSet(ViewSet):
    def create(self, request):
        crawler_name = request.data.get('name', None)
        if crawler_name:
            crawler_task.delay(crawler_name)
            return Response({'created': True})
        else:
            return Response({'created': False})


class DataViewSet(ViewSet):
    def list(self, request):
        config = ConfigParser()
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        config.read(os.path.join(__location__, 'settings.INI'))
        user = config['database.mongodb']['User']
        pwd = config['database.mongodb']['Pwd']
        source = config['database.mongodb']['Source']
        c = MongoClient()
        db = c[source]
        db.authenticate(user, pwd, source=source)
        collection = request.query_params.get('collection', None)
        p = request.query_params.get('page', None)
        if collection and collection in db.collection_names():
            coll = db[collection]
            if p:
                skip = int(p) * 100
                limit = (int(p) + 1) * 100
                results = coll.find({}, skip=skip, limit=limit)
            else:
                results = coll.find({})
            c.close()
            return Response(dumps(results))
        else:
            coll = db.collection_names()
            c.close()
            return Response(coll)
