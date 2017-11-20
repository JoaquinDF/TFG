import json

import pandas as pd
from utils.bot import Bot


# TODO: Parse dates
class BotInstance(Bot):
    collection = 'bots.fp7.projects'
    key = 'id'

    def process_item(self, db=None):
        url = 'http://cordis.europa.eu/data/cordis-fp7projects.xlsx'
        data = pd.read_excel(url)
        json_data = data.to_json(orient='records')
        docs = json.loads(json_data)
        for doc in docs:
            yield doc
