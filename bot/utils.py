import random
import string
import typing as t

import aiohttp


async def get_random_str(n: int):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


async def get_aiohttp_session(tokens: t.Dict):
    headers = {}
    if tokens.get('access'):
        headers = {"Authorization": f"Bearer {tokens['access']}"}
    return aiohttp.ClientSession(headers=headers)
