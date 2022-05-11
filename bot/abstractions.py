import typing as t

from abc import ABC, abstractmethod


class ClientAction(ABC):
    @abstractmethod
    async def request(self):
        raise NotImplemented()


class Generator(ABC):

    @property
    @abstractmethod
    def user_data(self) -> t.Dict:
        raise NotImplemented()

    @property
    @abstractmethod
    def text(self) -> t.Dict:
        raise NotImplemented()