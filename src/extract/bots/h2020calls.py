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
            collection = db[coll]
            bulk = collection.initialize_ordered_bulk_op()
            for doc in docs:
                bulk.find({'CallIdentifier.CallId': doc['CallIdentifier']['CallId']}).upsert().replace_one(doc)
            result = bulk.execute()

        return result
