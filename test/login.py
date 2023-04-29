from json import dumps

from tornado.escape import json_decode
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.web import Application

from api.handlers.login import LoginHandler
from .base import BaseTest


class LoginHandlerTest(BaseTest):

    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/login', LoginHandler)])
        super().setUpClass()

    @coroutine
    def register(self):
        yield self.get_app().db.users.insert_one({
            'email': self.email,
            'fullName': self.encrypt('testFullName'),
            'phoneNumber': self.encrypt('testPhoneNumber'),
            'disability': self.encrypt('testDisability'),
            'password': self.hash(self.password),
            'displayName': 'testDisplayName'
        })

    def setUp(self):
        super().setUp()

        self.email = 'test@test.com'
        self.password = 'testPassword'

        IOLoop.current().run_sync(self.register)

    def test_login(self):
        body = {
          'email': self.email,
          'password': self.password
        }

        response = self.fetch('/login', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertIsNotNone(body_2['token'])
        self.assertIsNotNone(body_2['expiresIn'])

    def test_login_case_insensitive(self):
        body = {
          'email': self.email.swapcase(),
          'password': self.password
        }

        response = self.fetch('/login', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertIsNotNone(body_2['token'])
        self.assertIsNotNone(body_2['expiresIn'])

    def test_login_wrong_email(self):
        body = {
          'email': 'wrongUsername',
          'password': self.password
        }

        response = self.fetch('/login', method='POST', body=dumps(body))
        self.assertEqual(403, response.code)

    def test_login_wrong_password(self):
        body = {
          'email': self.email,
          'password': 'wrongPassword'
        }

        response = self.fetch('/login', method='POST', body=dumps(body))
        self.assertEqual(403, response.code)
