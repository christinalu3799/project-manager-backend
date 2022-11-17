import models
 
from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
# arg1 = blueprints name
# arg2 = import name
project = Blueprint('projects','project')
# ================================================================
@project.route('/', methods=['GET'])
# @login_required
def get_all_projects():
    print('is current user authenticated?', current_user.is_authenticated)
    # find all projects and change each project from a dictionary to a new array
    try:
        projects = [model_to_dict(project) for project in current_user.projects]
        session['projects'] = projects
        # print(session['projects']) 
        print('trying to get projects!')
        return jsonify(data=session['projects'], status={
            'code': 200,
            'message': 'Successfully retrieved all projects!'
        })
    except models.DoesNotExist:
        print('sorry, cannot find projects!')
        return jsonify(data={}, status={
            'code': 401,
            'message': 'Sorry! Could not find projects.'
        })
# ================================================================
@project.route('/<id>', methods=['GET'])
# @login_required
def get_one_project(id):
    project = models.Project.get_by_id(id)
    return jsonify(
        data=model_to_dict(project),
        status=200,
        message=f"Successfully retrieved project with id of {id}"
    ), 200
# ================================================================
@project.route('/', methods = ['POST'])
# @login_required
def create_project():
    payload = request.get_json()
    project = models.Project.create(
        project_owner = current_user.id,
        project_name = payload['project_name'],
        project_deadline = payload['project_deadline'],
        project_description = payload['project_description'],
        project_status = payload['project_status']
    )
    project_dict = model_to_dict(project)
    return jsonify(data = project_dict, status = {
        'code': 201,
        'message': 'Successfully created a new project.'
    })
# ================================================================
@project.route('/<id>', methods = ['PUT'])
# @login_required
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
# @login_required
def delete_project(id):
    query = models.Project.delete().where(models.Project.id == id)
    query.execute()
    return jsonify(
        data = f"Successfully deleted project with id: {id}.",
        message = f"Successfully deleted project with id: {id}.",
        status = 200
    ), 200