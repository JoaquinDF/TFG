from __future__ import absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod


class Bot(object, metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        pass
