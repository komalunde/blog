import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
)

username = 'root'
password = 'root'
host = 'localhost'
port = '3306'
database = 'blog'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(username, password, host, port, database)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['you@example.com']
