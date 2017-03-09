from migrate.versioning import api
from config import eng
from config import SQLALCHEMY_MIGRATE_REPO
api.upgrade(eng,SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(eng,SQLALCHEMY_MIGRATE_REPO)
print ('Current database version:' +str(v))