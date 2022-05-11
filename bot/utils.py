import argparse
import json
import typing as t
import csv

import aiohttp

from bot.generator import RandomGenerator, CsvGenerator


async def get_aiohttp_session(tokens: t.Dict):
    headers = {}
    if tokens.get('access'):
        headers = {"Authorization": f"Bearer {tokens['access']}"}
    return aiohttp.ClientSession(headers=headers)


async def read_config():
    with open('config.json') as config_json:
        config = json.load(config_json)
        config_json.close()
    return config


async def read_csv(filename: str):
    file = open(filename)
    csv_reader = csv.reader(file)
    next(csv_reader)

    return csv_reader


async def get_generator():
    datasource_parser = argparse.ArgumentParser()
    datasource_parser.add_argument('--datasource',
                                   type=str,
                                   help='which generator is used')

    args = datasource_parser.parse_args()
    datasource = args.datasource

    if datasource == 'random':
        return RandomGenerator(15)

    elif datasource == 'csv':
        users_data = await read_csv('users_data.csv')
        texts = await read_csv('texts.csv')

        return CsvGenerator(users_data, texts)

    else:
        raise AttributeError('no datasource provided')
