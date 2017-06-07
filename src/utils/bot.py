import collections
from abc import ABCMeta, abstractmethod

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
            bulk = c.initialize_ordered_bulk_op()
            for doc in self.process_item(db=db):
                key = doc
                for s in self.key.split('.'):
                    key = key[s]
                bulk.find({self.key: key}).upsert().replace_one(doc)
            bulk.execute()
        return True
