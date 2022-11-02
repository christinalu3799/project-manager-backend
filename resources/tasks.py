import models
 
from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

# arg1 = blueprints name
# arg2 = import name
task = Blueprint('tasks','task')
# ================================================================
@task.route('/', methods=['GET'])
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
@task.route('/', methods=['POST'])
def create_task():
    payload = request.get_json()
    task = models.Task.create(**payload)
    print('model to dict', model_to_dict(task)) # change model to dict
    task_dict = model_to_dict(task)
    return jsonify(data=task_dict, status={
        'code': 201,
        'message': 'Successfully created a new task.'
    })