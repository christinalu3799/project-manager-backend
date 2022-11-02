from peewee import *
import datetime 

DATABASE = SqliteDatabase('projects.sqlite')

# ================================================================
'''
user_id (FOREIGN KEY)
project_name
project_deadline
*** project_files
project_description
project_tasks
project_status
project_logs

'''
class Project(Model):
    # user_id = ForeignKeyField(User, backred='projects')
    project_name = CharField()
    project_deadline = DateField() # 2022-11-2
    project_description = TextField()
    # project_tasks = ForeignKeyField(Task, backurl='tasks')
    project_status = CharField() # 'not started'/'in progress'/'completed'
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
    DATABASE.create_tables([Project, Task], safe=True)
    print("Connected to the DB and created tables if they don't already exist")
    DATABASE.close()
    
