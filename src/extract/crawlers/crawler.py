import logging
from utils.mongodb import Mongodb
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, error
from threading import Thread, Lock


def __init_reactor__():
    try:
        reactor.run(installSignalHandlers=0)
    except error.ReactorAlreadyRunning as e:
        logging.error(e)
        pass


def run(spider_instance):
    mongodb = Mongodb()
    runner = CrawlerRunner({
        'AUTOTHROTTLE_ENABLED': True,
        'ITEM_PIPELINES': {
            'extract.crawlers.pipelines.MongoPipeline': 300
        },
        'MONGO_USER': mongodb.user,
        'MONGO_PWD': mongodb.pwd,
        'MONGO_SRC': mongodb.source,
        'MONGO_COLL': spider_instance.collection
    })
    lock = Lock()
    lock.acquire()
    d = runner.crawl(spider_instance)
    d.addBoth(lambda _: lock.release())
    t = Thread(target=__init_reactor__)
    t.daemon = True
    t.start()
    lock.acquire()

    return True
