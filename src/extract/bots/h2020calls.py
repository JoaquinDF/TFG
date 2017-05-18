import json
import requests
from .bot import Bot
from utils.mongodb import Mongodb


class BotInstance(Bot):
    def run(self):
        url = 'http://ec.europa.eu/research/participants/portal/data/call/h2020/calls.json'
        response = requests.get(url=url)
        response.encoding = 'ISO-8859-1'

        coll = 'bots.h2020.calls'
        docs = json.loads(response.text)['callData']['Calls']

        with Mongodb() as mongodb:
            db = mongodb.db
            if coll not in db.collection_names():
                collection = db.create_collection(coll)
                collection.insert_many(docs)
            else:
                collection = db[coll]
                for doc in docs:
                    collection.replace_one({'CallIdentifier.CallId': doc['CallIdentifier']['CallId']}, doc, upsert=True)
