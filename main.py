import asyncio

import logging

from bot.bot import Bot
from bot.utils import get_generator, read_config


async def main():
    generator = await get_generator()

    config = await read_config()

    number_of_users = config.get('number_of_user')
    max_posts_per_user = config.get('max_posts_per_user')
    max_likes_per_user = config.get('max_likes_per_user')
    url = 'http://127.0.0.1:8000'

    logging.basicConfig(level=logging.INFO)
    bot = Bot(number_of_users, max_posts_per_user, max_likes_per_user, url, generator)
    await bot.create_users()


asyncio.run(main())
