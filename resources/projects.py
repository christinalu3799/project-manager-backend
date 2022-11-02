import models
 
from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

# arg1 = blueprints name
# arg2 = import name
project = Blueprint('projects','project')