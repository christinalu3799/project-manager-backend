from peewee import *
import datetime 
from flask_login import UserMixin

import os
from playhouse.db_url import connect # connect to db in heroku


if 'ON_HEROKU' in os.environ: 
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else: 
    DATABASE = SqliteDatabase('projects.sqlite')

# ================================================================
class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta: 
        database = DATABASE
# ================================================================
class Project(Model):
    project_owner = ForeignKeyField(User, backref='projects')
    project_name = CharField()
    project_deadline = DateField() # 2022-11-2
    project_description = TextField()
    project_status = CharField() 
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
# ================================================================
class Task(Model):
    project_id = ForeignKeyField(Project, backref='tasks')
    task = CharField()
    is_complete = BooleanField(default=False)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
# ================================================================
class Log(Model):
    project_id = ForeignKeyField(Project, backref='logs')
    log = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
# ================================================================
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Project, Task, Log, User], safe=True)
    print("Connected to the DB and created tables if they don't already exist")
    DATABASE.close()
    
