import json

import pandas as pd
from utils.bot import Bot


class BotInstance(Bot):
    collection = 'bots.h2020.organizations'
    key = 'key'

    def process_item(self, db=None):
        url = 'http://cordis.europa.eu/data/cordis-h2020projects.csv'
        projects = pd.read_csv(url, sep=';')
        url = 'http://cordis.europa.eu/data/cordis-h2020organizations.csv'
        organizations = pd.read_csv(url, sep=';')
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
