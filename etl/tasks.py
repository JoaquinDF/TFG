from __future__ import absolute_import, unicode_literals

from celery import shared_task
from importlib import import_module


@shared_task
def bot(bot_name):
    bot_instance = import_module('.bots.' + bot_name, __package__).BotInstance()
    result = bot_instance.start()
    return result
