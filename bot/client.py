import typing as t

import aiohttp
from aiohttp.client_exceptions import ServerConnectionError

import bot.exceptions as exc
from bot.abstractions import ClientAction


class Client:
    def __init__(self, action: ClientAction):
        self._action = action

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action: ClientAction):
        self._action = action

    async def request(self):
        try:
            await self._action.request()
        except ServerConnectionError:
            raise exc.SocialNetworkApiException('Api does not work')

class UserRegistry(ClientAction):
    def __init__(self,
                 session: aiohttp.ClientSession,
                 url: str,
                 data: t.Dict):
        self.session = session
        self.url = url
        self.data = data

    async def request(self):
        await self.session.post(self.url, data=self.data)
