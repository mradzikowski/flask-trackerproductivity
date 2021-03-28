from flask import request, jsonify, render_template
from . import bp
import backend.services.user as user_services


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/register', methods=['POST'])
def create_user():
    try:
        data_json = request.json
        body = user_services.create_user(data_json)
        return jsonify(body)
    except ValueError as e:
        return e


