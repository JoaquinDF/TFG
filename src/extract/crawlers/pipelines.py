from pymongo import MongoClient


class MongoPipeline(object):
    def __init__(self, user, pwd, src, coll):
        self.user = user
        self.pwd = pwd
        self.src = src
        self.coll = coll
        self.client = None
        self.collection = None

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
        if self.coll not in db.collection_names():
            self.collection = db.create_collection(self.coll)
        else:
            self.collection = db[self.coll]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.replace_one({'id': item['id']}, item, upsert=True)
        return item
