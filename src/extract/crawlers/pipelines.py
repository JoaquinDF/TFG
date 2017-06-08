import logging
from pymongo import MongoClient, errors


class MongoPipeline(object):
    def __init__(self, user, pwd, src, coll):
        self.user = user
        self.pwd = pwd
        self.src = src
        self.coll = coll
        self.client = None
        self.bulk = None

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
        db = self.client[self.src]
        db.authenticate(self.user, self.pwd, source=self.src)
        collection = db[self.coll]
        self.bulk = collection.initialize_ordered_bulk_op()

    def close_spider(self, spider):
        try:
            self.bulk.execute()
        except errors.BulkWriteError as bwe:
            logging.debug(bwe.details)
        except errors.InvalidOperation as e:
            logging.debug(e)
        finally:
            self.client.close()

    def process_item(self, item, spider):
        self.bulk.find({'id': item['id']}).upsert().replace_one(item)
        return item
