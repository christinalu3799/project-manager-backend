import models
 
from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

# arg1 = blueprints name
# arg2 = import name
project = Blueprint('projects','project')
# ================================================================
@project.route('/', methods=['GET'])
def get_all_projects():
    # find all projects and change each project from a dictionary to a new array
    try:
        projects = [model_to_dict(project) for project in models.Project.select()]
        print(projects)
        return jsonify(data=projects, status={
            'code': 200,
            'message': 'Successfully retrieved all projects!'
        })
    except models.DoesNotExist:
        return jsonify(data={}, status={
            'code': 401,
            'message': 'Sorry! Could not find projects.'
        })
# ================================================================
@project.route('/', methods=['POST'])
def create_project():
    payload = request.get_json()
    project = models.Project.create(**payload)
    print('model to dict', model_to_dict(project)) # change model to dict
    project_dict = model_to_dict(project)
    return jsonify(data=project_dict, status={
        'code': 201,
        'message': 'Successfully created a new project.'
    })
