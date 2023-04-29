from tornado.escape import json_decode
from tornado.web import Application

from api.handlers.welcome import WelcomeHandler
from .base import BaseTest


class WelcomeHandlerTest(BaseTest):

    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/welcome', WelcomeHandler)])
        super().setUpClass()

    def test_welcome(self):
        response = self.fetch('/welcome')
        self.assertEqual(200, response.code)

        body = json_decode(response.body)
        self.assertIsNotNone(body['message'])
