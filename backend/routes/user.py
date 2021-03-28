from flask import request, jsonify, render_template
from . import bp
import backend.services.user as user_services


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/user', methods=['POST'])
def create_user():
    try:
        data_json = request.json
        body = user_services.create_user(data_json)
        return jsonify(body)
    except ValueError as e:
        return e


@bp.route('/user', methods=['GET'])
def get_user():
    try:
        data_json = request.json
        return jsonify(user_services.get_user(data_json))
    except ValueError as e:
        return {"status": "fail", "message": e}


@bp.route('/user', methods=['DELETE'])
def delete_user():
    try:
        data_json = request.json
        return jsonify(user_services.delete_user(data_json))
    except ValueError as e:
        return {"status": "fail", "message": e}




