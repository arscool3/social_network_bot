import asyncio
import random
import typing as t

from bot.utils import get_aiohttp_session
from bot.client import Client, PostAction, GetAction
from bot.abstractions import Generator


class Bot:
    def __init__(self, number_of_users: int, max_posts: int, max_likes: int, url: str, generator: Generator):
        self.number_of_users = number_of_users
        self.max_posts = max_posts
        self.max_likes = max_likes
        self.url = url
        self.generator = generator

    async def create_users(self):
        user_tasks = []
        for i in range(self.number_of_users):
            session = await get_aiohttp_session({})
            client = Client(session=session)

            user = User(self.max_posts, self.max_likes, self.url, client, self.generator)
            user_tasks.append(asyncio.create_task(user.do_actions()))

        await asyncio.gather(*user_tasks)


class User:
    def __init__(self, max_posts: int, max_likes: int, url: str, client: Client, generator: Generator):
        self.posts = random.randint(1, max_posts)
        self.likes = random.randint(1, max_likes)
        self.url = url
        self._client = client
        self._generator = generator

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client: Client):
        self._client = client

    async def do_actions(self):

        tokens = await self.authenticate()
        await self.post_authenticate(tokens)

        await self.create_posts_tasks()

        number_of_posts = await self.get_number_of_posts()
        await self.create_likes_tasks(number_of_posts)

        await self._client.session.close()

    async def authenticate(self):

        user_data = self._generator.user_data
        await self.registry(user_data)
        tokens = await self.login(user_data)

        return tokens

    async def post_authenticate(self, tokens: t.Dict):
        await self._client.session.close()
        self._client.session = await get_aiohttp_session(tokens)

    async def create_posts_tasks(self):
        create_posts_tasks = []
        for _ in range(self.posts):
            text = self._generator.text
            create_posts_tasks.append(asyncio.create_task(self.create_posts(text)))

        await asyncio.gather(*create_posts_tasks)

    async def create_likes_tasks(self, number_of_posts: int):
        add_likes_tasks = []
        for _ in range(self.likes):
            post_number = random.randint(1, number_of_posts)
            add_likes_tasks.append(asyncio.create_task(self.add_likes(post_number)))

        await asyncio.gather(*add_likes_tasks)

    async def registry(self, user_data: t.Dict):
        action = PostAction(session=self._client.session,
                            url=f"{self.url}/api/register/",
                            data=user_data)
        await self.request(action)

    async def login(self, user_data: t.Dict):
        action = PostAction(session=self._client.session,
                            url=f"{self.url}/api/token/",
                            data=user_data)
        response = await self.request(action)
        return response

    async def create_posts(self, text):
        action = PostAction(session=self._client.session,
                            url=f"f{self.url}/api/posts/",
                            data=text)
        await self.request(action)

    async def add_likes(self, post_number):
        action = PostAction(session=self._client.session,
                            url=f"{self.url}/api/posts/{post_number}/like/",
                            data={})
        await self.request(action)

    async def get_number_of_posts(self):
        action = GetAction(session=self._client.session,
                           url=f"{self.url}/api/posts/")
        response = await self.request(action)
        return response['count']

    async def request(self, action):
        self._client.action = action
        response = await self._client.request()
        return response
