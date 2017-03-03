import imp
from migrate.versioning import api
from app import db
from config import eng
from config import SQLALCHEMY_MIGRATE_REPO

v = api.db_version(eng,SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' %(v+1))
tmp_module = imp.new_module('old_moddel')
old_model = api.create_model(eng,SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(eng,SQLALCHEMY_MIGRATE_REPO,tmp_module.meta, db.metadata)
open(migration,"wt".write(script))
api.upgrade(eng,SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(eng,SQLALCHEMY_MIGRATE_REPO)
print ('New migration saved as'+migration)
print ('current database version:'+str(v))