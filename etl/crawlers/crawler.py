from __future__ import absolute_import, unicode_literals

import os
from configparser import ConfigParser
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, error
from threading import Thread


def __init_reactor():
    try:
        reactor.run(installSignalHandlers=0)
    except error.ReactorAlreadyRunning:
        pass


def run(spider_instance):
    config = ConfigParser()
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    config.read(os.path.join(__location__, 'settings.INI'))

    user = config['database.mongodb']['User']
    pwd = config['database.mongodb']['Pwd']
    source = config['database.mongodb']['Source']

    runner = CrawlerRunner({
        'AUTOTHROTTLE_ENABLED': True,
        'ITEM_PIPELINES': {
            'etl.crawlers.pipelines.MongoPipeline': 300
        },
        'MONGO_USER': user,
        'MONGO_PWD': pwd,
        'MONGO_SRC': source,
        'MONGO_COLL': spider_instance.collection
    })
    runner.crawl(spider_instance)
    t = Thread(target=__init_reactor)
    t.daemon = True
    t.start()
