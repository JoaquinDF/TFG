import json

import pandas as pd
from utils.bot import Bot


class BotInstance(Bot):
    collection = 'bots.fp7.organizations'
    key = 'id'

    def process_item(self, db=None):
        url = 'http://cordis.europa.eu/data/cordis-fp7projects.xlsx'
        projects = pd.read_excel(url)
        url = 'http://cordis.europa.eu/data/cordis-fp7organizations.xlsx'
        organizations = pd.read_excel(url)
        ids = projects[['id', 'title']]
        d_ids = {}
        for i, row in ids.iterrows():
            d_ids[row['id']] = row['title']
        organizations['projectTitle'] = organizations.apply(lambda row: d_ids[row['projectID']], axis=1)
        json_data = organizations.to_json(orient='records')
        docs = json.loads(json_data)
        for doc in docs:
            doc['key'] = str(doc['id']) + str(doc['projectID'])
            yield doc
