from json import dumps, loads
from tornado.web import RequestHandler

class BaseHandler(RequestHandler):

    @property
    def db(self):
        return self.application.db


    @property
    def executor(self):
        return self.application.executor

    def decrypt(self, value):
        return self.application.fernet.decrypt(value).decode()

    def encrypt(self, value):
        return self.application.fernet.encrypt(str.encode(value, encoding="utf8"))

    def hash(self, value):
        return self.application.password_hasher.hash(value)

    def verify(self, hash_str, value):
        return self.application.password_hasher.verify(hash_str, value)

    def prepare(self):
        if self.request.body:
            try:
                json_data = loads(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                self.send_error(400, message='Unable to parse this bloody JSON.')
        self.response = dict()

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', '*')
        self.set_header('Access-Control-Allow-Headers', '*')

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'
        self.response = kwargs
        self.write_json()

    def write_json(self):
        output = dumps(self.response)
        self.write(output)

    def options(self):
        self.set_status(204)
        self.finish()

