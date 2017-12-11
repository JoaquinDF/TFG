import collections
from abc import ABCMeta, abstractmethod
from pymongo.operations import ReplaceOne

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
            requests = []
            limit = 1000
            for doc in self.process_item(db=db):
                key = doc
                for s in self.key.split('.'):
                    key = key[s]
                requests.append(ReplaceOne(filter={self.key: key}, replacement=doc, upsert=True))
                if len(requests) == limit:
                    mongodb.do_bulk_requests(requests=requests,collection=self.collection)
                    requests = []
            if len(requests) > 0:
                mongodb.do_bulk_requests(requests=requests, collection=self.collection)
        return True
