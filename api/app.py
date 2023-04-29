# Provides functions for interacting with the OS
import os
# Provides password hashing functionality
from argon2 import PasswordHasher
# Provides a way to execute code asynchronously using threads
from concurrent.futures import ThreadPoolExecutor
# Provides an asynchronous MongoDB driver
from motor import MotorClient
# Provides symmetric encryption using the AES algorithm
from cryptography.fernet import Fernet
# Provides a framework for building web applications
from tornado.web import Application
# Provides a way to load environment variables from a file
from dotenv import load_dotenv
# Import configuration variables
from .conf import MONGODB_HOST, MONGODB_DBNAME, WORKERS
# Import request handler classes
from .handlers.welcome import WelcomeHandler
from .handlers.registration import RegistrationHandler
from .handlers.login import LoginHandler
from .handlers.logout import LogoutHandler
from .handlers.user import UserHandler

class Application(Application):
    """
    The main application class, which inherits from the Tornado Application class.
    """

    def __init__(self):
        """
        Initializes the application and sets up its components.
        """
        # Define the request handlers for the application
        handlers = [
            (r'/students/?', WelcomeHandler),
            (r'/students/api/?', WelcomeHandler),
            (r'/students/api/registration', RegistrationHandler),
            (r'/students/api/login', LoginHandler),
            (r'/students/api/logout', LogoutHandler),
            (r'/students/api/user', UserHandler)
        ]

        # Set up the application settings
        settings = dict()
        super(Application, self).__init__(handlers, **settings)

        # Set up the database connection (hello)
        self.db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

        # Load the encryption key from an environment variable
        load_dotenv('secret.env')
        key = os.getenv('ENCRYPTION_KEY').encode('utf-8')

        # Set up the encryption, password hashing, and thread pool components
        self.fernet = Fernet(key)
        # The PasswordHasher() function creates an instance of the PasswordHasher class provided by the passlib library.
        # This class provides a simple interface for securely hashing passwords using a variety of algorithms
        # Such as Argon2, bcrypt, and PBKDF2.
        self.password_hasher = PasswordHasher()
        # By default, PasswordHasher uses the Argon2 algorithm with recommended settings
        # These include memory usage, parallelism, and iterations.
        # I want to modify the number of rounds and the size of the salt used in the hash function
        # I will attempt to pass arguments to the PasswordHasher constructor.
        self.executor = ThreadPoolExecutor(WORKERS)
