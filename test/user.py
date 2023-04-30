from json import dumps
# Import necessary modules
from tornado.escape import json_decode, utf8
from tornado.gen import coroutine
from tornado.httputil import HTTPHeaders
from tornado.ioloop import IOLoop
from tornado.web import Application

# Import UserHandler from api.handlers.user and BaseTest from .base
from api.handlers.user import UserHandler
from .base import BaseTest

import urllib.parse

# Define UserHandlerTest class, which inherits from BaseTest
class UserHandlerTest(BaseTest):

    # Class method to set up the Tornado web application
    @classmethod
    def setUpClass(self):
        # Add UserHandler to the app routes
        self.my_app = Application([(r'/user', UserHandler)])
        # Call setUpClass method from BaseTest
        super().setUpClass()

    # Asynchronous method to add a user to the database
    @coroutine
    def register(self):
        yield self.get_app().db.users.insert_one({
            'email': self.email,
            'fullName': self.encrypt(self.full_name),
            'phoneNumber': self.encrypt(self.phone_number),
            'disability': self.encrypt(self.disability_type),
            'password': self.hash(self.password),
            'displayName': self.display_name
        })

    # Asynchronous method to set a token for the user
    @coroutine
    def login(self):
        yield self.get_app().db.users.update_one({
            'email': self.email
        }, {
            '$set': { 'token': self.token, 'expiresIn': 2147483647 }
        })

    # Set up the test
    def setUp(self):
        # Call setUp method from BaseTest
        super().setUp()

        # Initialize variables for the user's email, full name, phone number, disability type, password, display name, and token
        self.email = 'test@test.com'
        self.full_name = 'testFullName'
        self.phone_number = 'testPhoneNumber'
        self.disability_type = 'testDisability'
        self.password = 'testPasswordxxxxxxxxxx'
        self.display_name = 'testDisplayName'
        self.token = 'testToken'

        # Add the user to the database and set a token
        IOLoop.current().run_sync(self.register)
        IOLoop.current().run_sync(self.login)

    # Test whether the UserHandler returns the correct user information when given a valid token
    def test_user(self):
        # Construct an HTTP header with the token
        headers = HTTPHeaders({'X-Token': self.token})
        # Fetch the user information from the /user endpoint with the HTTP header
        response = self.fetch('/user', headers=headers)
        # Check whether the response code is 200 (OK)
        self.assertEqual(200, response.code)
        # Decode the JSON response body
        body_2 = json_decode(response.body)
        # Check whether the returned email matches the expected email
        self.assertEqual(self.email, body_2['email'])
        self.assertEqual(self.full_name, body_2['fullName'])
        self.assertEqual(self.phone_number, body_2['phoneNumber'])
        self.assertEqual(self.disability_type, body_2['disability'])
        self.assertEqual(self.display_name, body_2['displayName'])

    def test_user_without_token(self):
        response = self.fetch('/user')
        self.assertEqual(400, response.code)

    def test_user_wrong_token(self):
        headers = HTTPHeaders({'X-Token': 'wrongToken'})

        response = self.fetch('/user')
        self.assertEqual(400, response.code)
