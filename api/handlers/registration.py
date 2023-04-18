from tornado.escape import json_decode, utf8
from tornado.gen import coroutine

from .base import BaseHandler


class RegistrationHandler(BaseHandler):

    @coroutine
    def post(self):
        try:
            body = json_decode(self.request.body)
            email = body['email'].lower().strip()
            print (email)
            if not isinstance(email, str):
                raise Exception()
            password = body['password']
            if not isinstance(password, str):
                raise Exception()
            display_name = body.get('displayName')
            if display_name is None:
                display_name = email
            if not isinstance(display_name, str):
                raise Exception()
            full_name = body.get('fullName', '')
            if not isinstance(full_name, str):
                raise Exception()
            phone_number = body.get('phoneNumber', '')
            if not isinstance(phone_number, str):
                raise Exception()
            disability_type = body.get('disability', '')
            if not isinstance(disability_type, str):
                raise Exception()
        except Exception as e:
            self.send_error(400, message='You must provide an email address, password and display name!')
            return

        if not email:
            self.send_error(400, message='The email address is invalid!')
            return

        if not password:
            self.send_error(400, message='The password is invalid!')
            return

        if not display_name:
            self.send_error(400, message='The display name is invalid!')
            return

        user = yield self.db.users.find_one({
          'email': email
        }, {})

        if user is not None:
            self.send_error(409, message='A user with the given email address already exists!')
            return

        yield self.db.users.insert_one({
            'email': email,
            'fullName': self.encrypt(full_name),
            'phoneNumber': self.encrypt(phone_number),
            'disability': self.encrypt(disability_type),
            'password': self.hash(password),
            'displayName': display_name
        })

        self.set_status(200)
        self.response['email'] = email
        self.response['displayName'] = display_name
        self.response['fullName'] = full_name
        self.response['phoneNumber'] = phone_number
        self.response['disability'] = disability_type
        self.write_json()
