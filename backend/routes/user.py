from flask import request, jsonify
from . import bp
import backend.services.user as user_services


@bp.route('/user', methods=['POST'])
def create_user():
    try:
        data_json = request.json
        body, status = user_services.create_user(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"status": "fail", "message": e}


@bp.route('/user', methods=['GET'])
def get_user():
    try:
        data_json = request.json
        body, status = user_services.get_user(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"status": "fail", "message": e}


@bp.route('/user', methods=['DELETE'])
def delete_user():
    try:
        data_json = request.json
        body, status = user_services.delete_user(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"status": "fail", "message": e}


@bp.route('/user/tasks', methods=['GET'])
def get_all_tasks_for_user():
    try:
        data_json = request.json
        body, status = user_services.get_all_tasks_for_user(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"status": "fail", "message": "Error while getting tasks for user"}


@bp.route('/user/tasks/active', methods=['GET'])
def get_all_active_tasks_for_user():
    try:
        data_json = request.json
        body, status = user_services.get_all_active_tasks_for_user(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"status": "fail", "message": "Error while getting active tasks for user"}



