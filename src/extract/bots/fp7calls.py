import json

import requests

from utils.bot import Bot


class BotInstance(Bot):
    collection = 'bots.fp7.calls'
    key = 'CallIdentifier.CallId'

    def process_item(self, db=None):
        url = 'http://ec.europa.eu/research/participants/portal/data/call/fp7/calls.json'
        response = requests.get(url=url)
        response.encoding = 'ISO-8859-1'
        docs = json.loads(response.text)['callData']['Calls']
        for doc in docs:
            yield doc
