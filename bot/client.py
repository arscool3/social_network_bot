import typing as t

import aiohttp
from aiohttp.client_exceptions import ServerConnectionError

import bot.exceptions as exc
from bot.abstractions import ClientAction


class Client:
    def __init__(self, session: aiohttp.ClientSession, action: ClientAction = None):
        self._action = action
        self._session = session

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session: aiohttp.ClientSession):
        self._session = session

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action: ClientAction):
        self._action = action

    async def request(self):
        try:
            response = await self._action.request()
            print(response)
            return response
        except ServerConnectionError:
            raise exc.SocialNetworkApiException('Api does not work')


class PostAction(ClientAction):
    def __init__(self,
                 session: aiohttp.ClientSession,
                 url: str,
                 data: t.Dict):
        self.session = session
        self.url = url
        self.data = data

    async def request(self):
        response = await self.session.post(self.url, data=self.data)
        json_response = await response.json()
        return json_response
