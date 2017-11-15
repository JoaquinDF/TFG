import collections
import logging
from abc import ABCMeta, abstractmethod
from pymongo.operations import ReplaceOne
from pymongo.errors import BulkWriteError, InvalidOperation

from utils.mongodb import Mongodb


class Bot(object, metaclass=ABCMeta):
    @property
    @abstractmethod
    def collection(self):
        pass

    @property
    @abstractmethod
    def key(self):
        pass

    @abstractmethod
    def process_item(self, db=None) -> collections.Iterable:
        pass

    def run(self):
        with Mongodb() as mongodb:
            db = mongodb.db
            c = db[self.collection]
            requests = []
            for doc in self.process_item(db=db):
                key = doc
                for s in self.key.split('.'):
                    key = key[s]
                requests.append(ReplaceOne(filter={self.key: key}, replacement=doc, upsert=True))
            try:
                c.bulk_write(requests)
            except BulkWriteError as bwe:
                logging.debug(bwe.details)
            except InvalidOperation as io:
                logging.debug(io)
        return True
