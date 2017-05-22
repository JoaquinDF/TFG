import json
import pandas as pd
from .bot import Bot
from utils.mongodb import Mongodb


class BotInstance(Bot):
    def run(self):
        url = 'http://cordis.europa.eu/data/cordis-h2020organizations.csv'
        data = pd.read_csv(url, sep=';', encoding='utf-8-sig')
        json_data = data.to_json(orient='records')

        coll = 'bots.h2020.organizations'
        docs = json.loads(json_data)

        with Mongodb() as mongodb:
            db = mongodb.db
            collection = db[coll]
            bulk = collection.initialize_ordered_bulk_op()
            for doc in docs:
                bulk.find({'id': doc['id']}).upsert().replace_one(doc)
            result = bulk.execute()

        return result
