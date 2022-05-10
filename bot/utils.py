import typing as t

import aiohttp


async def get_aiohttp_session(tokens: t.Dict):
    headers = {}
    if tokens.get('access'):
        headers = {"Authorization": f"Bearer {tokens['access']}"}
    return aiohttp.ClientSession(headers=headers)
