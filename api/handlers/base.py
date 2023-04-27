from json import dumps, loads
from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    # Set properties to access the database and executor objects in the application
    @property
    def db(self):
        return self.application.db

    @property
    def executor(self):
        return self.application.executor

    # Define methods to encrypt, decrypt, hash, and verify password strings
    def decrypt(self, value):
        return self.application.fernet.decrypt(value).decode()

    def encrypt(self, value):
        return self.application.fernet.encrypt(str.encode(value, encoding="utf8"))

    def hash(self, value):
        return self.application.password_hasher.hash(value)

    def verify(self, hash_str, value):
        return self.application.password_hasher.verify(hash_str, value)

    # Override prepare() method to parse incoming JSON data
    def prepare(self):
        if self.request.body:
            try:
                # Attempt to load JSON data
                json_data = loads(self.request.body)
                # Add parsed data to request arguments
                self.request.arguments.update(json_data)
            except ValueError:
                # Send error message if unable to parse JSON
                self.send_error(400, message='Unable to parse this bloody JSON.')
        # Create an empty response dictionary
        self.response = dict()

    # Set default headers for each response
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', '*')
        self.set_header('Access-Control-Allow-Headers', '*')

    # Override write_error() method to write response as JSON
    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'
        # Set response dictionary to error message
        self.response = kwargs
        # Write error message as JSON
        self.write_json()

    # Write response dictionary as JSON
    def write_json(self):
        output = dumps(self.response)
        self.write(output)

    # Define OPTIONS method to handle preflight requests
    def options(self):
        self.set_status(204)
        self.finish()

# This code defines a base handler class for Tornado web application.
# It includes utility methods to hash and verify passwords, encrypt and decrypt data, as well as parse incoming JSON data.
# It also sets default headers for each response, handles errors and writes responses as JSON.
# Finally, it defines an OPTIONS method to handle preflight requests.
