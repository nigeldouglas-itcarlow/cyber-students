from datetime import datetime
from time import mktime
from tornado.gen import coroutine

from .base import BaseHandler


class AuthHandler(BaseHandler):

    @coroutine
    def prepare(self):
        super(AuthHandler, self).prepare()

        if self.request.method == 'OPTIONS':
            return

        try:
            token = self.request.headers.get('X-Token')
            if not token:
              raise Exception()
        except:
            self.current_user = None
            self.send_error(400, message='You must provide a token!')
            return

        user = yield self.db.users.find_one({
            'token': token
        }, {
            'email': 1,
            'fullName': 1,
            'phoneNumber': 1,
            'disability': 1,
            'displayName': 1,
            'expiresIn': 1
        })

        if user is None:
            self.current_user = None
            self.send_error(403, message='Your token is invalid!')
            return

        current_time = mktime(datetime.now().utctimetuple())
        if current_time > user['expiresIn']:
            self.current_user = None
            self.send_error(403, message='Your token has expired!')
            return

        full_name = user.get('fullName', '')
        if full_name:
            full_name = self.decrypt(full_name)
        self.current_user = {
            'email': user['email'],
            'full_name': full_name,
            'phoneNumber': user['phone_number'],
            'disability': user['disability_type'],
            'display_name': user['display_name']
        }

        phone_number = user.get('phoneNumber', '')
        if phone_number:
            self.decrypt(phone_number)
        self.current_user = {
            'email': user['email'],
            'full_name': full_name,
            'phoneNumber': user['phone_number'],
            'disability': user['disability_type'],
            'display_name': user['display_name']
        }

        disability_type = user.get('fullName', '')
        if disability_type:
            self.decrypt(disability_type)
        self.disability_type = {
            'email': user['email'],
            'full_name': full_name,
            'phoneNumber': user['phone_number'],
            'disability': user['disability_type'],
            'display_name': user['display_name']
        }
