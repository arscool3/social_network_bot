import random
import string
import typing as t

from bot.abstractions import Generator


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

    # @staticmethod
    # def post_number(number_of_posts: int):
    #     return random.randint(1, number_of_posts)
    #
    # @staticmethod
    # def number_of_posts(max_posts: int):
    #     return random.randint(1, max_posts)
    #
    # @staticmethod
    # def number_of_likes(max_likes: int):
    #     return random.randint(1, max_likes)

    @staticmethod
    def get_random_str(n: int):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


class CsvGenerator(Generator):
    def __init__(self, users_data: t.List, texts: t.List):
        self._users_data = users_data
        self._texts = texts

    @property
    def user_data(self) -> t.Dict:
        return random.choice(self._users_data)

    @property
    def text(self) -> t.Dict:
        return random.choice(self._texts)
