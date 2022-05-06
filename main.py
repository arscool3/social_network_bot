import asyncio
import json

from bot.utils import get_aiohttp_session
from bot.bot_actions import bot_login, bot_registry, bot_add_likes_factory, bot_create_post_factory, get_number_of_posts


async def read_config():

    with open('config.json') as config_json:
        config = json.load(config_json)
        config_json.close()
    return config


async def bot(max_posts, max_likes):
    web_url = "http://127.0.0.1:8000"

    anonymous_session = await get_aiohttp_session({})
    token_data = await bot_registry(web_url, anonymous_session)
    tokens = await bot_login(web_url, token_data, anonymous_session)

    await anonymous_session.close()

    user_session = await get_aiohttp_session(tokens)
    await bot_create_post_factory(web_url, max_posts, user_session)

    number_of_posts = await get_number_of_posts(web_url, user_session)

    await bot_add_likes_factory(web_url, number_of_posts, max_likes, user_session)

    await user_session.close()


async def bot_factory():
    config = await read_config()

    number_of_user = config.get('number_of_user')
    max_posts_per_user = config.get('max_posts_per_user')
    max_likes_per_user = config.get('max_likes_per_user')

    bot_tasks = []
    for _ in range(number_of_user):
        bot_tasks.append(asyncio.create_task(bot(max_posts_per_user, max_likes_per_user)))
    await asyncio.gather(*bot_tasks)


asyncio.run(bot_factory())

