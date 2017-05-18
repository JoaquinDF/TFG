from abc import ABCMeta, abstractmethod


class Bot(object, metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        pass
