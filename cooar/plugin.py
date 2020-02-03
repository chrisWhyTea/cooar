from abc import ABC, abstractmethod


class CooarPlugin(ABC):
    @abstractmethod
    def prepare(self):
        raise NotImplementedError()

    @abstractmethod
    def collect(self):
        raise NotImplementedError()

    @abstractmethod
    def download(self):
        raise NotImplementedError()
