import os
import logging
from configparser import ConfigParser
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, InvalidOperation


class Mongodb(object):
    def __init__(self):
        config = ConfigParser()
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        config.read(os.path.join(__location__, 'settings.INI'))
        settings = config['database.mongodb']
        self.user = settings['User']
        self.pwd = settings['Pwd']
        self.source = settings['Source']

    def __enter__(self):
        self.__c__ = MongoClient()
        self.db = self.__c__[self.source]
        self.db.authenticate(self.user, self.pwd, source=self.source)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__c__.close()

    def do_bulk_requests(self, requests, collection, limit=1000):
        c = self.db[collection]
        chunks = [requests[x:x + limit] for x in range(0, len(requests), limit)]
        for chunk in chunks:
            try:
                c.bulk_write(chunk)
            except BulkWriteError as bwe:
                logging.debug(bwe.details)
            except InvalidOperation as io:
                logging.debug(io)
