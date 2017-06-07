import json

import requests

from utils.bot import Bot


class BotInstance(Bot):
    collection = 'bots.h2020.topics'
    key = 'topicId'

    def process_item(self, db=None):
        url = 'http://ec.europa.eu/research/participants/portal/data/call/h2020/h2020_topics.json'
        response = requests.get(url=url)
        response.encoding = 'ISO-8859-1'
        docs = json.loads(response.text)['topicData']['Topics']
        for doc in docs:
            yield doc
