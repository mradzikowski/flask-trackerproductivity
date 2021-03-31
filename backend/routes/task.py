from flask import request, jsonify
from . import bp
import backend.services.task as task_service


@bp.route('/task', methods=['POST'])
def create_task():
    try:
        data_json = request.json
        body, status = task_service.create_task(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"success": False, "message": "Error while creating object."}


@bp.route('/task', methods=['GET'])
def get_task():
    try:
        data_json = request.json
        body, status = task_service.get_task(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"success": False,
                "message": "Error while retrieving task from database."}


@bp.route('/task', methods=['DELETE'])
def delete_task():
    try:
        data_json = request.json
        body, status = task_service.delete_task(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"success": False,
                "message": "Error while deleting task object from database."}


@bp.route('/task/finish', methods=['PATCH'])
def finish_task():
    try:
        data_json = request.json
        body, status = task_service.finish_task(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"success": False,
                "message": "Error while finishing the task"}


@bp.route('/task/get/all', methods=['GET'])
def get_all_tasks():
    try:
        body, status = task_service.get_all_tasks()
        return jsonify(body), status
    except ValueError as e:
        return {"success": False, "message": "Error while retrieving all tasks"}