import os
import logging
from configparser import ConfigParser
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, error
from threading import Thread, Lock


def __init_reactor__():
    try:
        reactor.run(installSignalHandlers=False)
    except error.ReactorAlreadyRunning as e:
        logging.debug(e)
        pass


def __get_settings__(collection=None):
    config = ConfigParser()
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    config.read(os.path.join(__location__, 'settings.INI'))
    crawler_settings = config['extract.crawler']
    mongodb_settings = config['database.mongodb']
    settings = {
        'USER_AGENT': crawler_settings['UserAgent'],
        'ROBOTSTXT_OBEY': crawler_settings.getboolean('RobotsTxt'),
        'AUTOTHROTTLE_ENABLED': crawler_settings.getboolean('AutothrottleEnabled'),
        'AUTOTHROTTLE_START_DELAY': int(crawler_settings['AutothrottleStartDelay']),
        'AUTOTHROTTLE_MAX_DELAY': int(crawler_settings['AutothrottleMaxDelay']),
        'AUTOTHROTTLE_TARGET_CONCURRENCY': float(crawler_settings['AutothrottleTargetConcurrency']),
        'FEED_EXPORT_ENCODING': crawler_settings['FeedExportEncoding'],
        'LOG_LEVEL': crawler_settings['LogLevel'],
        'COOKIES_ENABLED': crawler_settings.getboolean('CookiesEnabled'),
        # 'DOWNLOAD_DELAY': int(crawler_settings['DownloadDelay']),
        'ITEM_PIPELINES': {
            'utils.pipelines.MongoPipeline': int(crawler_settings['MongoPipelines'])
        },
        'MONGO_USER': mongodb_settings['User'],
        'MONGO_PWD': mongodb_settings['Pwd'],
        'MONGO_SRC': mongodb_settings['Source'],
        'MONGO_COLL': collection,
    }
    return settings


# TODO: Fix memory error
def run(spider_instance):
    settings = __get_settings__(collection=spider_instance.collection)
    runner = CrawlerRunner(settings)
    lock = Lock()
    lock.acquire()
    d = runner.crawl(spider_instance)
    d.addBoth(lambda _: lock.release())
    t = Thread(target=__init_reactor__)
    t.daemon = True
    t.start()
    lock.acquire()
    return True
