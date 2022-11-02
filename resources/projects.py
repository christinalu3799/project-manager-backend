import models
 
from flask import Blueprint, jsonify, request
from flask_login import login_required
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
@project.route('/<id>', methods=['GET'])
def get_one_project(id):
    print('id of project to retrieve: ',id)
    project = models.Project.get_by_id(id)
    return jsonify(
        data=model_to_dict(project),
        status=200,
        message=f"Successfully retrieved project with id of {id}"
    ), 200
# ================================================================
@project.route('/', methods = ['POST'])
@login_required
def create_project():
    payload = request.get_json()
    project = models.Project.create(**payload)
    print('model to dict', model_to_dict(project)) # change model to dict
    project_dict = model_to_dict(project)
    return jsonify(data = project_dict, status = {
        'code': 201,
        'message': 'Successfully created a new project.'
    })
# ================================================================
@project.route('/<id>', methods = ['PUT'])
@login_required
def update_project(id):
    payload = request.get_json()
    query = models.Project.update(**payload).where(models.Project.id == id)
    query.execute()
    return jsonify(
        data = model_to_dict(models.Project.get_by_id(id)),
        status = 200,
        message = f"Successfully updated project with id: {id}."
    ),200
# ================================================================
@project.route('/<id>', methods=['DELETE'])
@login_required
def delete_project(id):
    query = models.Project.delete().where(models.Project.id == id)
    query.execute()
    return jsonify(
        data = f"Successfully deleted project with id: {id}.",
        message = f"Successfully deleted project with id: {id}.",
        status = 200
    ), 200