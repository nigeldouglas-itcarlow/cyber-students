from argon2 import PasswordHasher
from concurrent.futures import ThreadPoolExecutor
from cryptography.fernet import Fernet
from motor import MotorClient
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

from .conf import MONGODB_HOST, MONGODB_DBNAME, WORKERS


class BaseTest(AsyncHTTPTestCase):

    @classmethod
    def setUpClass(self):
        self.my_app.db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

        self.my_app.executor = ThreadPoolExecutor(WORKERS)
        # This is how I generated the key
        # I ran this from shell when the key needs recycling
        # key = Fernet.generate_key()
        # Same as app.py this key is presented in plaintext
        key = b'OfegPNE8TI_tXLoPA4iC3ibJeU-xrVFsmg0VYUgNh9I='
        # This package was included in the requirements.txt file
        # It offers a simple way of encrypting the data
        self.my_app.fernet = Fernet(key)
        # I added PasswordHasher as it was a highly-recommended hasher
        # This simply initiates the hasher
        self.my_app.password_hasher = PasswordHasher()

    def get_new_ioloop(self):
        return IOLoop.current()

    def get_app(self):
        return self.my_app

    def decrypt(self, value):
        return self.my_app.fernet.decrypt(value).decode()

    def encrypt(self, value):
        return self.my_app.fernet.encrypt(str.encode(value, encoding="utf8"))

    def hash(self, value):
        return self.my_app.password_hasher.hash(value)

    def setUp(self):
        super().setUp()
        self.get_app().db.users.drop()

    def tearDown(self):
        super().tearDown()
        self.get_app().db.users.drop()
