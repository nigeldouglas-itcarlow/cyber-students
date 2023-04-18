import click
from json import loads
from motor.motor_tornado import MotorClient
from tornado.gen import coroutine
from tornado.ioloop import IOLoop

from api.conf import MONGODB_HOST, MONGODB_DBNAME

@coroutine
def get_users(db):
  cur = db.users.find({}, {
    'email': 1,
    'fullName': 1,
    'phoneNumber': 1,
    'disability': 1,
    'password': 1,
    'displayName': 1,
  })
  docs = yield cur.to_list(length=None)
  print('There are ' + str(len(docs)) + ' registered users:')
  for doc in docs:
    click.echo(doc)

@click.group()
def cli():
    pass

@cli.command()
def list():
    db = MotorClient(**MONGODB_HOST)[MONGODB_DBNAME]
    IOLoop.current().run_sync(lambda: get_users(db))

if __name__ == '__main__':
    cli()
