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
        # Here is a stronger hashing process using the argon2id algorithm with tuned parameters.
        # argon2id algorithm is a hybrid of argon2i and argon2d algorithms, and is considered the most secure option for password hashing.
        self.password_hasher = argon2.PasswordHasher(
          time_cost=16, memory_cost=65536, parallelism=8, hash_len=32, salt_len=16)
        self.executor = ThreadPoolExecutor(WORKERS)

# I used a time cost of 16, which means that the algorithm will be run 2^16 times.
# The memory cost of 65536 means the algorithm will use 64 MB of memory.
# Finally, the hash length of 32 bytes will produce a longer and more secure hash.

# Increasing the strength of hashing makes it more difficult to crack passwords using brute-force/dictionary attacks.
# However, stronger hashing also means that it will take more time and resources to hash passwords
# This will slow down the authentication process dramatically
# Increasing strength of hashing requires more memory, which is a concern for systems with limited resources.

# It's generally important to strike a balance between security and performance when choosing a hashing algorithm
# I chose the most intensive parameters as this is simply a test lab environment
# I kept in mind that hashing is only one part. I forced the use of strong passwords
