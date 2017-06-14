import json

import pandas as pd

from utils.bot import Bot


class BotInstance(Bot):
    collection = 'bots.h2020.projects'
    key = 'id'

    def process_item(self, db=None):
        url = 'http://cordis.europa.eu/data/cordis-h2020projects.xlsx'
        data = pd.read_excel(url)
        json_data = data.to_json(orient='records')
        docs = json.loads(json_data)
        for doc in docs:
            yield doc
