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

#pagination
POSTS_PER_PAGE =3
username = 'root'
password = 'root'
host = 'localhost'
port = '3306'
database = 'blog'

CRSF_ENABLED = True
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(username, password, host, port, database)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')

MAX_SEARCH_RESULTS = 50


MAIL_SERVER = 'smtp.googlemail.com'  #'localhost'
MAIL_PORT = 465
MAIL_USE_TLS =False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('komalunde228@')
MAIL_PASSWORD = os.environ.get('komal228@')


# administrator list
ADMINS = ['your-gmail-username@gmail.com']
