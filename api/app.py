import os
from argon2 import PasswordHasher
from concurrent.futures import ThreadPoolExecutor
from motor import MotorClient
from cryptography.fernet import Fernet
from dotenv import load_dotenv
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

# Load environment variables from secret.env file
load_dotenv('secret.env')

# Get the encryption key from the environment variables
encryption_key = os.getenv('ENCRYPTION_KEY')
print('Encryption key:', encryption_key)

# Decode the encryption key from a string to bytes
key = encryption_key.encode('utf-8')

# Perform a simple test using the encryption key
# Generate a random message
message = b'This is a test message'

# Encrypt the message using the encryption key
fernet = Fernet(key)
encrypted_message = fernet.encrypt(message)

# Decrypt the message using the encryption key
decrypted_message = fernet.decrypt(encrypted_message)

# Print the original message and the decrypted message
print('Original message:', message)
print('Decrypted message:', decrypted_message)
