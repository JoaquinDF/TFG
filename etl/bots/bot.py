import os
from configparser import ConfigParser
from abc import ABCMeta, abstractmethod


class Bot(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        config = ConfigParser()
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        config.read(os.path.join(__location__, 'settings.INI'))
        self.user = config['database.mongodb']['User']
        self.pwd = config['database.mongodb']['Pwd']
        self.source = config['database.mongodb']['Source']

    @abstractmethod
    def start(self):
        pass
