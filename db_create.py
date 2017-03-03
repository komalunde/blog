from migrate.versioning import api
from config import eng
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

db.create_all()
if not eng.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO,'database repository')
    api.version_control(eng,SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(eng,SQLALCHEMY_MIGRATE_REPO,api.version(SQLALCHEMY_MIGRATE_REPO))