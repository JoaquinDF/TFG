from __future__ import absolute_import, unicode_literals

import json
import pandas as pd
from .bot import Bot
from pymongo import MongoClient


class BotInstance(Bot):

    def start(self):
        url = 'http://cordis.europa.eu/data/cordis-h2020organizations.csv'
        data = pd.read_csv(url, sep=';', encoding='utf-8-sig')
        json_data = data.to_json(orient='records')

        coll = 'bots.h2020.organizations'
        docs = json.loads(json_data)

        c = MongoClient()
        db = c[self.source]
        db.authenticate(self.user, self.pwd, source=self.source)
        if coll not in db.collection_names():
            collection = db.create_collection(coll)
            collection.insert_many(docs)
        else:
            collection = db[coll]
            for doc in docs:
                collection.replace_one({'id': doc['id']}, doc, upsert=True)
        c.close()
        return True
