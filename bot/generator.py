import random
import string


class RandomGenerator:

    def __init__(self, size: int):
        self.size = size

    @property
    def email(self):
        email = self.get_random_str(self.size)
        return email + '@gmail.com'

    @property
    def login(self):
        return self.get_random_str(self.size)

    @property
    def password(self):
        return self.get_random_str(self.size)

    @property
    def title(self):
        return self.get_random_str(self.size)

    @staticmethod
    def post_number(number_of_posts: int):
        return random.randint(1, number_of_posts)

    @staticmethod
    def number_of_posts(max_posts: int):
        return random.randint(1, max_posts)

    @staticmethod
    def number_of_likes(max_likes: int):
        return random.randint(1, max_likes)

    @staticmethod
    def get_random_str(n: int):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
