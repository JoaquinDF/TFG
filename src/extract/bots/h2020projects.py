import json
import pandas as pd
from .bot import Bot
from utils.mongodb import Mongodb


class BotInstance(Bot):
    def run(self):
        url = 'http://cordis.europa.eu/data/cordis-h2020projects.csv'
        data = pd.read_csv(url, sep=';', encoding='utf-8-sig')
        json_data = data.to_json(orient='records')

        coll = 'bots.h2020.projects'
        docs = json.loads(json_data)

        with Mongodb() as mongodb:
            db = mongodb.db
            if coll not in db.collection_names():
                collection = db.create_collection(coll)
                collection.insert_many(docs)
            else:
                collection = db[coll]
                for doc in docs:
                    collection.replace_one({'id': doc['id']}, doc, upsert=True)
