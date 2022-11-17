import models
 
from flask import Blueprint, jsonify, request
from flask_login import login_required
from playhouse.shortcuts import model_to_dict

# arg1 = blueprints name
# arg2 = import name
log = Blueprint('logs','log')
# ================================================================
@log.route('/<project_id>', methods=['GET'])
# @login_required
def get_all_logs(project_id):
    try:
        logs = [model_to_dict(log) for log in models.Log.select().where(models.Log.project_id == project_id)]
        return jsonify(data=logs, status={
            'code': 200,
            'message': 'Successfully retrieved all logs!'
        })
    except models.DoesNotExist:
        return jsonify(data={}, status={
            'code': 401,
            'message': 'Sorry! Could not find logs.'
        })
# ================================================================
@log.route('/<project_id>', methods=['POST'])
# @login_required
def create_log(project_id):
    payload = request.get_json()
    log = models.Log.create(
        project_id = project_id,
        log = payload['log']
    )
    log_dict = model_to_dict(log)
    return jsonify(data=log_dict, status={
        'code': 201,
        'message': 'Successfully created a new log.'
    })
# ================================================================
@log.route('/<project_id>/<log_id>', methods = ['PUT'])
# @login_required
def update_log(project_id, log_id):
    payload = request.get_json()
    query = models.Log.update(**payload).where(models.Log.id == log_id, models.Log.project_id == project_id)
    query.execute()
    return jsonify(
        data = model_to_dict(models.Log.get_by_id(log_id)),
        status = 200,
        message = f"Successfully updated log with id: {log_id}."
    ),200
# ================================================================
@log.route('/<project_id>/<log_id>', methods=['DELETE'])
# @login_required
def delete_log(project_id, log_id):
    query = models.Log.delete().where(models.Log.id == log_id, models.Log.project_id == project_id)
    query.execute()
    return jsonify(
        data = f"Successfully deleted log with id: {log_id}.",
        message = f"Successfully deleted log with id: {log_id}.",
        status = 200
    ), 200