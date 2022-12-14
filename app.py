from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

import models
# ================================================================
# importing from resources
from resources.projects import project
from resources.tasks import task
from resources.user import user
from resources.logs import log
# ================================================================
import os
from dotenv import load_dotenv
load_dotenv()
DEBUG = True
PORT = int(os.environ.get('PORT', 8000))
FRONTEND_URL = os.environ.get('FRONTEND_URL')
# ================================================================
# Initialize instance of the Flask class 
app = Flask(__name__)
# ================================================================
# session settings for deployment 
# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='None',
# )
# ================================================================
login_manager = LoginManager()
login_manager.init_app(app) # set up session on the app
app.secret_key = os.environ.get('APP_SECRET')

@login_manager.user_loader
def load_user(userid):
    try: 
        print('------IM IN USER LOADER: ------', models.User.get(models.User.id == userid))
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None 
# ================================================================
# CORS - allow frontend to 'talk' to backend
# CORS(user, origins=["*"], supports_credentials=True)
# CORS(project, origins=["*"], supports_credentials=True)
# CORS(task, origins=["*"], supports_credentials=True)
# CORS(log, origins=["*"], supports_credentials=True)
CORS(user, origins=['http://localhost:3000', FRONTEND_URL], supports_credentials=True)
CORS(project, origins=['http://localhost:3000', FRONTEND_URL], supports_credentials=True)
CORS(task, origins=['http://localhost:3000', FRONTEND_URL], supports_credentials=True)
CORS(log, origins=['http://localhost:3000', FRONTEND_URL], supports_credentials=True)
# set up directions to handle api routes
app.register_blueprint(user, url_prefix='/api/v1/users')
app.register_blueprint(project, url_prefix='/api/v1/projects')
app.register_blueprint(task, url_prefix='/api/v1/projects/tasks')
app.register_blueprint(log, url_prefix='/api/v1/projects/logs')
# ================================================================
# connect to the database before each request
@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
# close the database connection after each request
@app.after_request
def after_request(response):
    g.db.close()
    return response 
# ================================================================
# initialize models if in development
if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()

# Run the app
if __name__=='__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)