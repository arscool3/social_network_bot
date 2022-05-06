import asyncio
import random
import typing as t

import aiohttp
from aiohttp.client_exceptions import ServerConnectionError

import bot.exceptions as exc
from bot.utils import get_random_str


async def bot_registry(web_url: str, session: aiohttp.ClientSession) -> t.Dict:
    login = await get_random_str(15)
    password = await get_random_str(15)
    registry_url = web_url + "/api/register/"
    data = {'username': login,
            'password': password,
            'email': f'{login}@gmail.com'}

    try:
        async with session.post(registry_url, data=data) as registry_response:
            if registry_response.status == 201:
                return {'username': login,
                        'password': password}
    except ServerConnectionError:
        raise exc.SocialNetworkApiException('Api does not work')


async def bot_login(web_url: str, token_data: t.Dict, session: aiohttp.ClientSession) -> t.Dict:
    token_url = web_url + "/api/token/"

    try:
        async with session.post(token_url, data=token_data) as token_response:
            json_token_response = await token_response.json()
            return {'access': json_token_response['access'],
                    'refresh': json_token_response['refresh']}
    except ServerConnectionError:
        raise exc.SocialNetworkApiException('Api does not work')


async def bot_create_posts_factory(web_url: str, max_posts: int, session: aiohttp.ClientSession):

    bot_create_posts_tasks = []
    for _ in range(random.randint(1, max_posts)):
        bot_create_posts_tasks.append(asyncio.create_task(bot_create_posts(web_url, session)))
    await asyncio.gather(*bot_create_posts_tasks)


async def bot_create_posts(web_url: str, session: aiohttp.ClientSession):
    posts_url = web_url + "/api/posts/"

    text = await get_random_str(50)

    try:
        await session.post(posts_url, data={'text': text})
    except ServerConnectionError:
        raise exc.SocialNetworkApiException('Api does not work')


async def bot_add_likes_factory(web_url: str, number_of_posts: int, max_likes: int, session: aiohttp.ClientSession):
    bot_add_likes_tasks = []

    for _ in range(random.randint(1, max_likes)):
        bot_add_likes_tasks.append(asyncio.create_task(bot_add_likes(web_url, number_of_posts, session)))

    await asyncio.gather(*bot_add_likes_tasks)


async def bot_add_likes(web_url: str, number_of_posts: int, session: aiohttp.ClientSession):
    post_number = random.randint(1, number_of_posts)
    like_url = web_url + f"/api/posts/{post_number}/like/"

    try:
        await session.post(like_url)
    except ServerConnectionError:
        raise exc.SocialNetworkApiException('Api does not work')


async def get_number_of_posts(web_url: str, session: aiohttp.ClientSession) -> int:
    try:
        async with session.get(web_url + f"/api/posts") as posts_response:
            posts_response_json = await posts_response.json()
            number_of_posts = posts_response_json.get('count')
            return number_of_posts or 0
    except ServerConnectionError:
        raise exc.SocialNetworkApiException('Api does not work')
