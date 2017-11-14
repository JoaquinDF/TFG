import epo_ops
import xmltodict
import json

from utils.bot import Bot


class BotInstance(Bot):
    collection = 'bots.epo.patents'
    key = ''

    def process_item(self, db=None):
        pass