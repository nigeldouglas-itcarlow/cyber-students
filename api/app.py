from argon2 import PasswordHasher
from concurrent.futures import ThreadPoolExecutor
from motor import MotorClient
from cryptography.fernet import Fernet
from tornado.web import Application

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

        self.db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

        # I intend to call this file from a secure location - ie: KMS (Key Management System)
        # This is the encryption key. It's not normal behaviour to load this into the code
        # In my next commit, I intend to load this from a file locally
        key = b'OfegPNE8TI_tXLoPA4iC3ibJeU-xrVFsmg0VYUgNh9I='

        self.fernet = Fernet(key)

        self.password_hasher = PasswordHasher()

        self.executor = ThreadPoolExecutor(WORKERS)
