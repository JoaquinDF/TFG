import os
from configparser import ConfigParser
from pymongo import MongoClient


class Mongodb(object):
    def __init__(self):
        config = ConfigParser()
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        config.read(os.path.join(__location__, 'settings.INI'))
        settings = config['database.mongodb']
        self.user = settings['User']
        self.pwd = settings['Pwd']
        self.source = settings['Source']

    def __enter__(self):
        self.__c__ = MongoClient()
        self.db = self.__c__[self.source]
        self.db.authenticate(self.user, self.pwd, source=self.source)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__c__.close()
