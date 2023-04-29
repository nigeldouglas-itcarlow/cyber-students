import re
from tornado.escape import json_decode, utf8
from tornado.gen import coroutine
from datetime import datetime

from .base import BaseHandler


class RegistrationHandler(BaseHandler):

    # Define a coroutine to handle HTTP POST requests for user registration
    @coroutine
    def post(self):
        try:
            # Parse the JSON request body into a Python dictionary
            body = json_decode(self.request.body)
            # Extract and clean the email field
            email = body['email'].lower().strip()
            print(email)
            # Check that email is a string
            if not isinstance(email, str):
                raise Exception()
            # Extract and validate the password field
            password = body['password']
            if not isinstance(password, str):
                raise Exception()
            # Extract and validate the display name field
            display_name = body.get('displayName')
            if display_name is None:
                display_name = email
            if not isinstance(display_name, str):
                raise Exception()
            # Extract and validate the full name field
            full_name = body.get('fullName', '')
            if not isinstance(full_name, str):
                raise Exception()
            # Extract and validate the phone number field
            phone_number = body.get('phoneNumber', '')
            if not isinstance(phone_number, str):
                raise Exception()
            # Extract and validate the disability field
            disability_type = body.get('disability', '')
            if not isinstance(disability_type, str):
                raise Exception()
        except Exception as e:
            # If any required field is missing or invalid, return a 400 Bad Request error with a message
            self.send_error(400, message='You must provide an email address, password and display name!')
            return
        # Check that email field is not empty
        if not email:
            self.send_error(400, message='The email address is invalid!')
            return
        # if an empty password, it also throws as 404 error
        if not password:
            self.send_error(400, message='The password is invalid!')
            return
        # Check that password meets complexity requirements
        password_pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{6,}$')
        if not password_pattern.match(password):
            self.send_error(400, message='The password must contain at least one uppercase letter, one lowercase letter, and one digit, and be at least 6 characters long.')
            return
        # Check that password is at least 14 characters long
        if len(password) < 14:
            self.send_error(400, message='The password must be at least 14 characters long!')
            return

        if not display_name:
            self.send_error(400, message='The display name is invalid!')
            return

        user = yield self.db.users.find_one({
          'email': email
        }, {})
        # If user already exists, return a 409 Conflict error with a message
        if user is not None:
            self.send_error(409, message='A user with the given email address already exists!')
            return
        # adds the day of the week and date automatically
        now = datetime.now()
        day_of_week = now.strftime('%A')
        date = now.strftime('%d/%m/%Y')
        # If all validation checks pass, insert new user record into the database
        yield self.db.users.insert_one({
            'email': email,
            'fullName': self.encrypt(full_name),
            'phoneNumber': self.encrypt(phone_number),
            'disability': self.encrypt(disability_type),
            'password': self.hash(password),
            'displayName': display_name,
            'dayOfWeek': day_of_week,
            'date': date
        })
        # Set HTTP status code to 200 OK
        self.set_status(200)
        # Add response fields to a dictionary
        self.response['email'] = email
        self.response['displayName'] = display_name
        self.response['fullName'] = full_name
        self.response['phoneNumber'] = phone_number
        self.response['disability'] = disability_type
        self.response['dayOfWeek'] = day_of_week
        self.response['date'] = date
        self.write_json()
