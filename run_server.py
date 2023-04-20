from logging import basicConfig, INFO, info
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from api.app import Application
from api.conf import PORT


def main():
    basicConfig(level=INFO)

    http_server = HTTPServer(Application())
    http_server.listen(PORT)

    info('Nigel has a server starting on port ' + str(PORT) + '...')
    IOLoop.current().start()


if __name__ == '__main__':
    main()
