from peewee import *
import datetime 
from flask_login import UserMixin
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
    project_status = CharField() # 'not started'/'in progress'/'completed'
    # project_tasks = ForeignKeyField(Task, backref='projects')
    # project_logs = ForeignKeyField(Log, backref='logs')
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
# ================================================================
class Task(Model):
    project_id = ForeignKeyField(Project, backref='tasks')
    task = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
# ================================================================
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Project, Task, User], safe=True)
    print("Connected to the DB and created tables if they don't already exist")
    DATABASE.close()
    
