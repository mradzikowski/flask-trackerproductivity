from flask import request, jsonify, render_template
from . import bp
import backend.services.user as user_services


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/register', methods=['POST'])
def create_user():
    username = request.form['username']
    email = request.form['email']
    print(f"DATA:, {username}, {email}")
    data_json = {"username": username, "email": email}
    body = user_services.create_user(data_json)
    return jsonify(body)