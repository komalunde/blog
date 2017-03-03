WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

from sqlalchemy import create_engine
import os
basedir = os.path.abspath(os.path.dirname(__file__))

eng = create_engine("mysql+pymysql://root:root@localhost/testdb")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# conn = eng.connect()
# conn.execute("commit")
# conn.execute("create database testdb")
# conn.close()
