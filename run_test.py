import logging
import unittest

from test.login import LoginHandlerTest
from test.logout import LogoutHandlerTest
from test.registration import RegistrationHandlerTest
from test.user import UserHandlerTest
from test.welcome import WelcomeHandlerTest

if __name__ == '__main__':
    logging.getLogger('tornado.access').disabled = True
    unittest.main()
