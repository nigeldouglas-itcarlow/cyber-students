from json import dumps
from tornado.escape import json_decode, utf8
from tornado.gen import coroutine
from tornado.httputil import HTTPHeaders
from tornado.ioloop import IOLoop
from tornado.web import Application

from api.handlers.user import UserHandler

from .base import BaseTest

import urllib.parse

class UserHandlerTest(BaseTest):

    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/user', UserHandler)])
        super().setUpClass()

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

    @coroutine
    def login(self):
        yield self.get_app().db.users.update_one({
            'email': self.email
        }, {
            '$set': { 'token': self.token, 'expiresIn': 2147483647 }
        })

    def setUp(self):
        super().setUp()

        self.email = 'test@test.com'
        self.full_name = 'testFullName'
        self.phone_number = 'testPhoneNumber'
        self.disability_type = 'testDisability'
        self.password = 'testPassword'
        self.display_name = 'testDisplayName'
        self.token = 'testToken'

        IOLoop.current().run_sync(self.register)
        IOLoop.current().run_sync(self.login)

    def test_user(self):
        headers = HTTPHeaders({'X-Token': self.token})

        response = self.fetch('/user', headers=headers)
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
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
