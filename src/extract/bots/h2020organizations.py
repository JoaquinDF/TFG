import json

import pandas as pd

from extract.bots.bot import Bot


class BotInstance(Bot):
    collection = 'bots.h2020.organizations'
    key = 'id'

    def process_item(self, db=None):
        url = 'http://cordis.europa.eu/data/cordis-h2020organizations.csv'
        data = pd.read_csv(url, sep=';', encoding='utf-8-sig')
        json_data = data.to_json(orient='records')
        docs = json.loads(json_data)
        for doc in docs:
            yield doc
