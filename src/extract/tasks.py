from __future__ import absolute_import, unicode_literals

import logging
from importlib import import_module
from celery import shared_task
from utils import crawler


@shared_task
def bot_task(bot_name):
    logging.info('bot_task - {}: started'.format(bot_name))
    b = import_module('.bots.' + bot_name, __package__).BotInstance()
    r = b.run()
    return {'name': bot_name, 'finished': r}


@shared_task
def crawler_task(spider_name):
    logging.info('crawler_task - {}: started'.format(spider_name))
    s = import_module('.crawlers.' + spider_name, __package__).SpiderInstance
    r = crawler.run(s)
    return {'name': spider_name, 'finished': r}
