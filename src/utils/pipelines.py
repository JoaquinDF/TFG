import logging
from pymongo import MongoClient
from pymongo.operations import ReplaceOne
from pymongo.errors import BulkWriteError, InvalidOperation


class MongoPipeline(object):
    def __init__(self, user, pwd, src, coll):
        self.user = user
        self.pwd = pwd
        self.src = src
        self.coll = coll
        self.client = None
        self.db = None
        self.requests = []
        self.limit = 1000


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


    def close_spider(self, spider):
        if len(self.requests) > 0:
            try:
                c = self.db[self.coll]
                c.bulk_write(self.requests)
            except BulkWriteError as bwe:
                logging.debug(bwe.details)
            except InvalidOperation as io:
                logging.debug(io)
            finally:
                self.client.close()


    def process_item(self, item, spider):
        self.requests.append(ReplaceOne(filter={'id': item['id']}, replacement=item, upsert=True))
        if len(self.requests) >= self.limit:
            c = self.db[self.coll]
            c.bulk_write(self.requests)
            self.requests = []
        return item
