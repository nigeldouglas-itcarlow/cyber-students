# Import necessary libraries
from argon2 import PasswordHasher
from concurrent.futures import ThreadPoolExecutor
from cryptography.fernet import Fernet
from motor import MotorClient
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase

# Import configuration parameters from the conf.py file
from .conf import MONGODB_HOST, MONGODB_DBNAME, WORKERS


# Create a base test case class that inherits from AsyncHTTPTestCase
class BaseTest(AsyncHTTPTestCase):

    # Class method that is run once at the beginning of all tests
    @classmethod
    def setUpClass(self):
        # Connect to the MongoDB database specified in the configuration
        self.my_app.db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]

        # Create a thread pool executor with the number of workers specified in the configuration
        self.my_app.executor = ThreadPoolExecutor(WORKERS)

        # Generate a Fernet key or use a pre-generated one from configuration
        key = b'OfegPNE8TI_tXLoPA4iC3ibJeU-xrVFsmg0VYUgNh9I='

        # Create a Fernet object using the key to encrypt and decrypt data
        self.my_app.fernet = Fernet(key)

        # Create a PasswordHasher object to hash and verify passwords
        self.my_app.password_hasher = PasswordHasher()

    # Method that returns the current IOLoop
    def get_new_ioloop(self):
        return IOLoop.current()

    # Method that returns the current Tornado application object
    def get_app(self):
        return self.my_app

    # Method that decrypts a given value using the Fernet object
    def decrypt(self, value):
        return self.my_app.fernet.decrypt(value).decode()

    # Method that encrypts a given value using the Fernet object
    def encrypt(self, value):
        return self.my_app.fernet.encrypt(str.encode(value, encoding="utf8"))

    # Method that hashes a given value using the PasswordHasher object
    def hash(self, value):
        return self.my_app.password_hasher.hash(value)

    # Method that is run before each test to drop the users collection in the database
    def setUp(self):
        super().setUp()
        self.get_app().db.users.drop()

    # Method that is run after each test to drop the users collection in the database
    def tearDown(self):
        super().tearDown()
        self.get_app().db.users.drop()
