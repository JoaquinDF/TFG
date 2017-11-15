import logging
from pymongo import MongoClient
from pymongo.operations import ReplaceOne
from pymongo.errors import BulkWriteError, InvalidOperation


#TODO: initialize_ordered_bulk_op deprecated, cambiar!!!
class MongoPipeline(object):
    def __init__(self, user, pwd, src, coll):
        self.user = user
        self.pwd = pwd
        self.src = src
        self.coll = coll
        self.client = None
        self.db = None
        # self.bulk = None
        self.requests = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user=crawler.settings.get('MONGO_USER'),
            pwd=crawler.settings.get('MONGO_PWD'),
            src=crawler.settings.get('MONGO_SRC'),
            coll=crawler.settings.get('MONGO_COLL')
        )

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client[self.src]
        self.db.authenticate(self.user, self.pwd, source=self.src)
        # collection = db[self.coll]
        # self.bulk = collection.initialize_ordered_bulk_op()

    def close_spider(self, spider):
        try:
            # self.bulk.execute()
            c = self.db[self.coll]
            c.bulk_write(self.requests)
        except BulkWriteError as bwe:
            logging.debug(bwe.details)
        except InvalidOperation as io:
            logging.debug(io)
        finally:
            self.client.close()

    def process_item(self, item, spider):
        # self.bulk.find({'id': item['id']}).upsert().replace_one(item)
        self.requests.append(ReplaceOne(filter={'id': item['id']}, replacement=item, upsert=True))
        return item
