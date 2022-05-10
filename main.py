import asyncio
import json
import logging

from bot.bot import Bot


async def read_config():
    with open('config.json') as config_json:
        config = json.load(config_json)
        config_json.close()
    return config


async def main():
    config = await read_config()

    number_of_users = config.get('number_of_user')
    max_posts_per_user = config.get('max_posts_per_user')
    max_likes_per_user = config.get('max_likes_per_user')
    url = 'http://127.0.0.1:8000'

    logging.basicConfig(level=logging.INFO)
    bot = Bot(number_of_users, max_posts_per_user, max_likes_per_user, url)
    await bot.create_users()


asyncio.run(main())
