from flask import jsonify, request

import backend.services.user as user_services

from . import bp


@bp.route('/user', methods=['POST', 'GET'])
def create_user():
    if request.method == "POST":
        data_json = request.json
        body, status = user_services.create_user(data_json)
    elif request.method == "GET":
        body, status = user_services.get_all_users()
    else:
        body, status = None, 405

    return jsonify(body), status


@bp.route('/user/<pk>', methods=['GET', 'DELETE'])
def get_user(pk):
    if request.method == "GET":
        body, status = user_services.get_user(pk)
    elif request.method == "DELETE":
        body, status = user_services.delete_user(pk)
    else:
        body, status = None, 405

    return jsonify(body), status


@bp.route('/user/<pk>/tasks', methods=['GET'])
def get_all_tasks_for_user(pk):
    if request.method == "GET":
        active = request.args.get('active')

        if active is None:
            body, status = user_services.get_all_tasks_for_user(pk)
        if active.upper() == "TRUE":
            active = True
        elif active.upper() == "FALSE":
            active = False
        else:
            return {"success": False, "message": "Invalid argument key."}, 400

        body, status = user_services.get_all_active_tasks_for_user(pk, active)
    else:
        body, status = None, 405
    return jsonify(body), status


@bp.route('/user/<pk>/tasks/productivity', methods=['GET'])
def get_productivity_for_user(pk):
    if request.method == "GET":
        body, status = user_services.get_all_tasks_and_calculate_productivity(pk)
    else:
        body, status = None, 405
    return jsonify(body), status


@bp.route('/user/get/all', methods=['GET'])
def get_all_users():
    if request.methdod == "GET":
        body, status = user_services.get_all_users()
    else:
        body, status = None, 405
    return jsonify(body), status


