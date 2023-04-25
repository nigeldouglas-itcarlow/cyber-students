import os  # Provides functions for interacting with the operating system
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

from .conf import MONGODB_HOST, MONGODB_DBNAME, WORKERS  # Import configuration variables
from .handlers.welcome import WelcomeHandler  # Import request handler classes
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

        # Set up the database connection
        self.db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

        # Load the encryption key from an environment variable
        load_dotenv('secret.env')
        key = os.getenv('ENCRYPTION_KEY').encode('utf-8')

        # Set up the encryption, password hashing, and thread pool components
        self.fernet = Fernet(key)
        self.password_hasher = PasswordHasher()
        self.executor = ThreadPoolExecutor(WORKERS)
