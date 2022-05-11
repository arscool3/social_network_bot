import random
import string
import typing as t

from bot.abstractions import Generator
from bot.exceptions import NotEnoughDataException


class RandomGenerator(Generator):

    def __init__(self, size: int):
        self.size = size

    @property
    def user_data(self) -> t.Dict:
        login = self.get_random_str(self.size)
        email = self.get_random_str(self.size) + '@gmail.com'
        password = self.get_random_str(self.size)
        return {'username': login, 'email': email, 'password': password}

    @property
    def text(self) -> t.Dict:
        return {'text': self.get_random_str(self.size)}

    @staticmethod
    def get_random_str(n: int):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


class CsvGenerator(Generator):
    def __init__(self, users_data_reader, texts_reader):
        self._users_data_reader = users_data_reader
        self._texts_reader = texts_reader

    @property
    def user_data(self) -> t.Dict:
        try:
            user_data_list = next(self._users_data_reader)
        except StopIteration:
            raise NotEnoughDataException('Not enough rows in users_data.csv file')
        try:
            return {'username': user_data_list[0],
                    'password': user_data_list[1],
                    'email': user_data_list[2],
                    }
        except IndexError:
            raise NotEnoughDataException('Not enough attributes in users_data.csv file')

    @property
    def text(self) -> t.Dict:
        try:
            text_list = next(self._texts_reader)
        except StopIteration:
            raise NotEnoughDataException('Not enough rows in texts.csv file')
        try:
            return {'text': text_list[0]}
        except IndexError:
            raise NotEnoughDataException('Not enough attributes in texts.csv file')

