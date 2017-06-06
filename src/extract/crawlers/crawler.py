import logging
from utils.mongodb import Mongodb
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, error
from threading import Thread, Lock


def __init_reactor__():
    try:
        reactor.run(installSignalHandlers=False)
    except error.ReactorAlreadyRunning as e:
        logging.debug(e)
        pass


def run(spider_instance):
    mongodb = Mongodb()
    runner = CrawlerRunner({
        'USER_AGENT': 'crawler (+http://www.bisite.usal.es)',
        'ROBOTSTXT_OBEY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_LEVEL': 'INFO',
        'COOKIES_ENABLED': False,
        # 'DOWNLOAD_DELAY': 2,
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
