# Import necessary modules
from datetime import datetime
from time import mktime
from tornado.gen import coroutine

# Import the BaseHandler class
from .base import BaseHandler

# Define the AuthHandler class
class AuthHandler(BaseHandler):

    # Coroutine that gets called before every request
    @coroutine
    def prepare(self):

        # Call the parent class's prepare method
        super(AuthHandler, self).prepare()

        # If the request method is OPTIONS, return
        if self.request.method == 'OPTIONS':
            return

        try:
            # Get the token from the request headers
            token = self.request.headers.get('X-Token')

            # Raise an exception if the token is missing
            if not token:
              raise Exception()

        # Catch the exception and return an error response
        except:
            self.current_user = None
            self.send_error(400, message='You must provide a token!')
            return

        # Query the database for the user associated with the token
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

        # If no user is found, return an error response
        if user is None:
            self.current_user = None
            self.send_error(403, message='Your token is invalid!')
            return

        # Check if the token has expired
        current_time = mktime(datetime.now().utctimetuple())
        if current_time > user['expiresIn']:
            self.current_user = None
            self.send_error(403, message='Your token has expired!')
            return

        # Decrypt certain user fields and create a current user object
        full_name = user.get('fullName', '')
        if full_name:
            full_name = self.decrypt(full_name)
        phone_number = user.get('phoneNumber', '')
        if phone_number:
            phone_number = self.decrypt(phone_number)
        disability_type = user.get('disability', '')
        if disability_type:
            disability_type = self.decrypt(disability_type)
        self.current_user = {
            'email': user['email'],
            'full_name': full_name,
            'phone_number': phone_number,
            'disability_type': disability_type,
            'display_name': user['displayName']
        }

# This is a Python code module defines an AuthHandler class that inherits from the BaseHandler class.
# The prepare() method gets called before every request and performs authentication by checking;
# 1. If a token is present in the request headers and querying the DB for the associated user.
# 2. If the token is missing or invalid, an error response is returned.
