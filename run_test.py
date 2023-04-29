import logging
import unittest

if __name__ == '__main__':
    logging.getLogger('tornado.access').disabled = True
    unittest.main()
