from json import dumps
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import Application

from api.handlers.registration import RegistrationHandler

from .base import BaseTest

import urllib.parse

class RegistrationHandlerTest(BaseTest):

    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/registration', RegistrationHandler)])
        super().setUpClass()

    def test_registration(self):
        email = 'test@test.com'
        full_name = 'testFullName'
        phone_number = 'testPhoneNumber'
        disability_type = 'testDisability'
        display_name = 'testDisplayName'

        body = {
          'email': email,
          'fullName': full_name,
          'phoneNumber': phone_number,
          'disability': disability_type,
          'password': 'testPassword',
          'displayName': display_name
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(email, body_2['email'])
        self.assertEqual(full_name, body_2['fullName'])
        self.assertEqual(phone_number, body_2['phoneNumber'])
        self.assertEqual(disability_type, body_2['disability'])
        self.assertEqual(display_name, body_2['displayName'])

    def test_registration_without_display_name(self):
        email = 'test@test.com'

        body = {
          'email': email,
          'password': 'testPassword'
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(email, body_2['email'])
        self.assertEqual(email, body_2['displayName'])

    def test_registration_twice(self):
        body = {
          'email': 'test@test.com',
          'password': 'testPassword',
          'displayName': 'testDisplayName'
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        response_2 = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(409, response_2.code)
