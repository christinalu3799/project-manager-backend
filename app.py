from flask import Flask, g, jsonify
import os
import models
from dotenv import load_dotenv
load_dotenv()

DEBUG = True
PORT = os.environ.get('PORT')

# Initialize instance of the Flask class 
app = Flask(__name__)
# ======================================================
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
# ======================================================

@app.route('/')
def index(): 
    return jsonify(name='Christina', age=23)

# Run the app
if __name__=='__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)