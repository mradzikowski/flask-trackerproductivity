from flask import jsonify, request

import backend.services.task as task_service

from . import bp


@bp.route('/task', methods=['GET', 'POST'])
def create_task():
    if request.method == "GET":
        body, status = task_service.get_all_tasks()
    elif request.method == "POST":
        data_json = request.json
        body, status = task_service.create_task(data_json)
    else:
        body, status = None, 405
    return jsonify(body), status


@bp.route('/task/<int:pk>', methods=['GET', 'DELETE'])
def delete_task(pk):
    if request.method == "GET":
        body, status = task_service.get_task(pk)
    elif request.method == "DELETE":
        body, status = task_service.delete_task(pk)
    else:
        body, status = None, 405

    return jsonify(body), status


@bp.route('/task/<int:pk>/finish', methods=['PATCH'])
def finish_task(pk):
    if request.method == "PATCH":
        body, status = task_service.finish_task(pk)
    else:
        body, status = None, 405
    return jsonify(body), status


@bp.route('/task/get/all', methods=['GET'])
def get_all_tasks():
    if request.method == "GET":
        body, status = task_service.get_all_tasks()
    else:
        body, status = None, 405
    return jsonify(body), status


@bp.route('/task/user/<pk>/week', methods=['GET'])
def get_tasks_from_last_week(pk):
    if request.method == "GET":
        body, status = task_service.get_tasks_from_last_week(pk)
    else:
        body, status = None, 405
    return jsonify(body), status
