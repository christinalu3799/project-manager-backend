import models
 
from flask import Blueprint, jsonify, request
from flask_login import login_required
from playhouse.shortcuts import model_to_dict

# arg1 = blueprints name
# arg2 = import name
task = Blueprint('tasks','task')
# ================================================================
@task.route('/', methods=['GET'])
@login_required
def get_all_tasks():
    try:
        tasks = [model_to_dict(task) for task in models.Task.select()]
        print(tasks)
        return jsonify(data=tasks, status={
            'code': 200,
            'message': 'Successfully retrieved all tasks!'
        })
    except models.DoesNotExist:
        return jsonify(data={}, status={
            'code': 401,
            'message': 'Sorry! Could not find tasks.'
        })
# ================================================================
@task.route('/<id>', methods = ['PUT'])
@login_required
def update_task(id):
    payload = request.get_json()
    query = models.Task.update(**payload).where(models.Task.id == id)
    query.execute()
    return jsonify(
        data = model_to_dict(models.Task.get_by_id(id)),
        status = 200,
        message = f"Successfully updated task with id: {id}."
    ),200
# ================================================================
@task.route('/<project_id>', methods=['POST'])
@login_required
def create_task(project_id):
    payload = request.get_json()
    task = models.Task.create(
        project_id = project_id,
        task = payload['task']
    )
    print('model to dict', model_to_dict(task)) # change model to dict
    task_dict = model_to_dict(task)
    return jsonify(data=task_dict, status={
        'code': 201,
        'message': 'Successfully created a new task.'
    })
# ================================================================
@task.route('/<id>', methods=['DELETE'])
@login_required
def delete_task(id):
    query = models.Task.delete().where(models.Task.id == id)
    query.execute()
    return jsonify(
        data = f"Successfully deleted task with id: {id}.",
        message = f"Successfully deleted task with id: {id}.",
        status = 200
    ), 200