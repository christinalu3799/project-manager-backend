from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = True
PORT = os.environ.get('PORT')

# Initialize instance of the Flask class 
app = Flask(__name__)

@app.route('/')
def index(): 
    return 'hi'


# Run the app
if __name__=='__main__':
    app.run(debug=DEBUG, port=PORT)