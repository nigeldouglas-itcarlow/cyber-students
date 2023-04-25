# Import necessary modules
from json import dumps
from tornado.escape import json_decode
from tornado.web import Application

# Import RegistrationHandler from api.handlers.registration module
from api.handlers.registration import RegistrationHandler

# Import BaseTest class from current package
from .base import BaseTest

# Define RegistrationHandlerTest as a subclass of BaseTest
class RegistrationHandlerTest(BaseTest):

    # Define setUpClass method to set up a test Application
    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/registration', RegistrationHandler)])
        super().setUpClass()

    # Define a test for registration with a full set of input data
    def test_registration(self):
        email = 'test@test.com'
        full_name = 'testFullName'
        phone_number = 'testPhoneNumber'
        disability_type = 'testDisability'
        display_name = 'testDisplayName'

        # Set up the request body with input data
        body = {
          'email': email,
          'fullName': full_name,
          'phoneNumber': phone_number,
          'disability': disability_type,
          'password': 'testPassword',
          'displayName': display_name
        }

        # Send a POST request to the /registration endpoint with the input data
        response = self.fetch('/registration', method='POST', body=dumps(body))

        # Assert that the response code is 200 (OK)
        self.assertEqual(200, response.code)

        # Parse the response body as JSON and assert that the output data matches the input data
        body_2 = json_decode(response.body)
        self.assertEqual(email, body_2['email'])
        self.assertEqual(full_name, body_2['fullName'])
        self.assertEqual(phone_number, body_2['phoneNumber'])
        self.assertEqual(disability_type, body_2['disability'])
        self.assertEqual(display_name, body_2['displayName'])

    # Define a test for registration without a display name
    def test_registration_without_display_name(self):
        email = 'test@test.com'

        # Set up the request body with input data (excluding display name)
        body = {
          'email': email,
          'password': 'testPassword'
        }

        # Send a POST request to the /registration endpoint with the input data
        response = self.fetch('/registration', method='POST', body=dumps(body))

        # Assert that the response code is 200 (OK)
        self.assertEqual(200, response.code)

        # Parse the response body as JSON and assert that the display name is set to the email address
        body_2 = json_decode(response.body)
        self.assertEqual(email, body_2['email'])
        self.assertEqual(email, body_2['displayName'])

    # Define a test for attempting to register the same user twice
    def test_registration_twice(self):
        # Set up the request body with input data
        body = {
          'email': 'test@test.com',
          'password': 'testPassword',
          'displayName': 'testDisplayName'
        }

        # Send a POST request to the /registration endpoint with the input data
        response = self.fetch('/registration', method='POST', body=dumps(body))

        # Assert that the response code is 200 (OK)
        self.assertEqual(200, response.code)

        # Attempt to register the same user again with the same input data
        response_2 = self.fetch('/registration', method='POST', body=dumps(body))

        # Assert that the response code is 409 (Conflict), indicating that the user already exists
        self.assertEqual(409, response_2.code)
