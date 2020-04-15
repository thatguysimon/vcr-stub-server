from abc import ABC, abstractmethod


class BaseVcrCassette(ABC):
    @abstractmethod
    def response_for(self, method: str, url: str, body: str, headers: list):
        pass
