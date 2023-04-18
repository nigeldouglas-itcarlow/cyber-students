from gitinfo import get_git_info
from os import environ

from .base import BaseHandler

class WelcomeHandler(BaseHandler):

    def get(self):
        self.set_status(200)
        self.response['message'] = 'Welcome to the Nigel Douglas Cryptography Lab!'
        git_commit_hash = environ.get('GIT_COMMIT_HASH')
        if git_commit_hash:
            self.response['commit'] = git_commit_hash
        else:
            git_info = get_git_info()
            if git_info:
                self.response['commit'] = git_info['commit']
            else:
                self.response['commit'] = 'UNKNOWN'
        self.write_json()
