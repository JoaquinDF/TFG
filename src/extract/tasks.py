from __future__ import absolute_import, unicode_literals
from importlib import import_module
from celery import shared_task

from .crawlers import crawler


@shared_task
def bot_task(bot_name):
    b = import_module('.bots.' + bot_name, __package__).BotInstance()
    b.run()
    return True


@shared_task
def crawler_task(spider_name):
    s = import_module('.crawlers.' + spider_name, __package__).SpiderInstance
    crawler.run(s)
    return True
