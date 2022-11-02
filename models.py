from peewee import *
import datetime 

DATABASE = SqliteDatabase('projects.sqlite')


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
    project_deadline = DateField()
    project_description = TextField()
    # project_tasks = ForeignKeyField(Task, backurl='tasks')
    project_status = CharField() # 'not started'/'in progress'/'completed'
    # project_logs = ForeignKeyField(Log, backref='logs')
    created_date = DateTimeField(default=datetime.datetime.now)
