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
        login = self.get_random_str(self.size)
        return login

    @property
    def password(self):
        password = self.get_random_str(self.size)
        return password

    @property
    def title(self):
        title = self.get_random_str(self.size)
        return title

    def post_number(self, number_of_posts):
        return random.randint(1, number_of_posts)

    @staticmethod
    def get_random_str(n: int):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
