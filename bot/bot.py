import random
import asyncio
import time

from bot.utils import get_aiohttp_session, get_random_str
from bot.client import Client, PostAction


class Bot:
    def __init__(self, number_of_users: int, max_posts: int, max_likes: int):
        self.number_of_users = number_of_users
        self.max_posts = max_posts
        self.max_likes = max_likes

    async def create_users(self):
        user_tasks = []
        for i in range(self.number_of_users):
            user = User(random.randint(1, self.max_posts),
                        random.randint(1, self.max_likes))  # todo remove logic
            user_tasks.append(asyncio.create_task(user.do_actions()))
        await asyncio.gather(*user_tasks)


class User:
    def __init__(self, number_of_posts: int, number_of_likes: int):
        self.posts = number_of_posts
        self.likes = number_of_likes

    async def do_actions(self):
        login = await get_random_str(15)
        password = await get_random_str(15)
        session = await get_aiohttp_session(tokens={})
        await self.registry(session, login, password)
        await self.login(session, login, password)

    @staticmethod
    async def registry(session, login, password):

        client_registry = PostAction(session=session,
                                     url="http://127.0.0.1:8000/api/register/",
                                     data={'username': login,
                                           'password': password,
                                           'email': f'{login}@gmail.com'})
        client = Client(action=client_registry)
        await client.request()

        # await session.close()

    @staticmethod
    async def login(session, login, password):
        client_login = PostAction(session=session,
                                  url="http://127.0.0.1:8000/api/login/",
                                  data={'username': login,
                                        'password': password})
        client = Client(action=client_login)
        await client.request()

        await session.close()
