from tornado.web import authenticated

from .auth import AuthHandler

class UserHandler(AuthHandler):

    @authenticated
    def get(self):
        self.set_status(200)
        self.response['email'] = self.current_user['email']
        self.response['fullName'] = self.current_user['full_name']
        self.response['phoneNumber'] = self.current_user['phone_number']
        self.response['disability'] = self.current_user['disability_type']
        self.response['displayName'] = self.current_user['display_name']
        self.write_json()
