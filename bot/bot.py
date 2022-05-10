import asyncio
import typing as t

from bot.utils import get_aiohttp_session
from bot.client import Client, PostAction, GetAction
from bot.generator import RandomGenerator


class Bot:
    def __init__(self, number_of_users: int, max_posts: int, max_likes: int):
        self.number_of_users = number_of_users
        self.max_posts = max_posts
        self.max_likes = max_likes

    async def create_users(self):
        user_tasks = []
        for i in range(self.number_of_users):
            session = await get_aiohttp_session({})
            client = Client(session=session)

            random_generator = RandomGenerator(15)

            user = User(self.max_posts, self.max_likes, client, random_generator)
            user_tasks.append(asyncio.create_task(user.do_actions()))

        await asyncio.gather(*user_tasks)


class User:
    def __init__(self, max_posts: int, max_likes: int, client: Client, random_generator: RandomGenerator):
        self.posts = RandomGenerator.number_of_posts(max_posts)
        self.likes = RandomGenerator.number_of_likes(max_likes)
        self._client = client
        self._random_generator = random_generator

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
        login = self._random_generator.login
        password = self._random_generator.password

        await self.registry(login, password)
        tokens = await self.login(login, password)

        return tokens

    async def post_authenticate(self, tokens: t.Dict):
        await self._client.session.close()
        self._client.session = await get_aiohttp_session(tokens)

    async def create_posts_tasks(self):
        create_posts_tasks = []
        for _ in range(self.posts):
            title = self._random_generator.title
            create_posts_tasks.append(asyncio.create_task(self.create_posts(title)))

        await asyncio.gather(*create_posts_tasks)

    async def create_likes_tasks(self, number_of_posts: int):
        add_likes_tasks = []
        for _ in range(self.likes):
            post_number = self._random_generator.post_number(number_of_posts)
            add_likes_tasks.append(asyncio.create_task(self.add_likes(post_number)))

        await asyncio.gather(*add_likes_tasks)

    async def registry(self, login: str, password: str):
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
        response = await self.request(action)
        return response

    async def create_posts(self, text):
        action = PostAction(session=self._client.session,
                            url="http://127.0.0.1:8000/api/posts/",
                            data={'text': text})
        await self.request(action)

    async def add_likes(self, post_number):
        action = PostAction(session=self._client.session,
                            url=f"http://127.0.0.1:8000/api/posts/{post_number}/like/",
                            data={})
        await self.request(action)

    async def get_number_of_posts(self):
        action = GetAction(session=self._client.session,
                           url="http://127.0.0.1:8000/api/posts/")
        response = await self.request(action)
        return response['count']

    async def request(self, action):
        self._client.action = action
        response = await self._client.request()
        return response
