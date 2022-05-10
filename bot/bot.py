import random
import asyncio
import time

import aiohttp

from bot.utils import get_aiohttp_session, get_random_str
from bot.client import Client, PostAction


class Bot:
    def __init__(self, number_of_users: int, max_posts: int, max_likes: int):
        self.number_of_users = number_of_users
        self.max_posts = max_posts
        self.max_likes = max_likes

    async def create_users(self):
        user_tasks = []
        session = await get_aiohttp_session({})
        client = Client(session=session)
        for i in range(self.number_of_users):
            user = User(random.randint(1, self.max_posts),
                        random.randint(1, self.max_likes),
                        client=client,
                        )  # todo remove logic
            user_tasks.append(asyncio.create_task(user.do_actions()))
        await asyncio.gather(*user_tasks)


class User:
    def __init__(self, number_of_posts: int, number_of_likes: int, client: Client):
        self.posts = number_of_posts
        self.likes = number_of_likes
        self._client = client

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client: Client):
        self._client = client

    async def do_actions(self):
        login = await get_random_str(15)
        password = await get_random_str(15)
        await self.registry(login, password)
        tokens = await self.login(login, password)

        await self._client.session.close()
        self._client.session = await get_aiohttp_session(tokens)

        create_posts_tasks = []
        for _ in range(self.posts):
            create_posts_tasks.append(asyncio.create_task(self.create_posts('abcd')))
        await asyncio.gather(*create_posts_tasks)

        add_likes_tasks = []
        for _ in range(self.likes):
            add_likes_tasks.append(asyncio.create_task(self.add_likes()))

        await asyncio.gather(*add_likes_tasks)

        await self._client.session.close()

    async def registry(self, login, password):
        action = PostAction(session=self._client.session,
                            url="http://127.0.0.1:8000/api/register/",
                            data={'username': login,
                                  'password': password,
                                  'email': f'{login}@gmail.com'})
        await self.request(action)

    async def login(self, login, password):
        action = PostAction(session=self._client.session,
                            url="http://127.0.0.1:8000/api/token/",
                            data={'username': login,
                                  'password': password})
        await self.request(action)

    async def create_posts(self, text):
        action = PostAction(session=self._client.session,
                            url="http://127.0.0.1:8000/api/posts/",
                            data={'text': text})
        await self.request(action)

    async def add_likes(self):
        action = PostAction(session=self._client.session,
                            url="http://127.0.0.1:8000/api/posts/10/like/",
                            data={})
        await self.request(action)

    async def request(self, action):
        self._client.action = action
        await self._client.request()
