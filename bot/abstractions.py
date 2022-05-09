from abc import ABC, abstractmethod


class Client(ABC):
    @abstractmethod
    def request(self):
        pass
