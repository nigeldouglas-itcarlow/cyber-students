import os
import argon2
from concurrent.futures import ThreadPoolExecutor
from motor import motor_asyncio as ma
from cryptography.fernet import Fernet
from tornado.web import Application
from dotenv import load_dotenv
from .conf import MONGODB_HOST, MONGODB_DBNAME, WORKERS
from .handlers.welcome import WelcomeHandler
from .handlers.registration import RegistrationHandler
from .handlers.login import LoginHandler
from .handlers.logout import LogoutHandler
from .handlers.user import UserHandler

class Application(Application):

    def __init__(self):
        handlers = [
            (r'/students/?', WelcomeHandler),
            (r'/students/api/?', WelcomeHandler),
            (r'/students/api/registration', RegistrationHandler),
            (r'/students/api/login', LoginHandler),
            (r'/students/api/logout', LogoutHandler),
            (r'/students/api/user', UserHandler)
        ]

        settings = dict()
        super(Application, self).__init__(handlers, **settings)

        self.db = ma.AsyncIOMotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

        load_dotenv('secret.env')
        key = os.getenv('ENCRYPTION_KEY').encode('utf-8')

        # Set up the encryption, password hashing, and thread pool components
        self.fernet = Fernet(key)
        self.password_hasher = argon2.PasswordHasher(
            time_cost=4, memory_cost=102400, parallelism=8, hash_len=16, salt_len=16)
        self.executor = ThreadPoolExecutor(WORKERS)
