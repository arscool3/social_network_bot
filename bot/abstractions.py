from abc import ABC, abstractmethod


class ClientAction(ABC):
    @abstractmethod
    async def request(self):
        pass
