from abc import ABC, abstractmethod


class BaseService(ABC):

    @abstractmethod
    def init(self, *args, **kwargs):
        pass
