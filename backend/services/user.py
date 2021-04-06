import re
from datetime import datetime

from sqlalchemy import exc

from backend.extensions import db
from backend.models.user import User, user_schema, users_schema
from backend.services.helper import (get_all_tasks_activity,
                                     is_email_registered, is_registered)


def create_user(data_json):
    try:
        if not data_json:
            return {"success": False, "message": "No data provided"}, 400

        if is_registered(data_json['username']):
            return {"success": False,
                    "message": "Username has been already taken"}, 400

        if is_email_registered(data_json['email']):
            return {"success": False,
                    "message": "Email is used in this service."}, 400

        data = user_schema.load(data_json)
        regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.search(regex, data['email']):
            return {"success": False, "message": "Invalid format of email"}
        new_user = User(**data)
        new_user.registered = datetime.now()
        db.session.add(new_user)
        db.session.commit()

        return {"success": True, "data": user_schema.dump(new_user)}, 201
    except ValueError as e:
        return {"success": False, "message": "Error while creating the user"}, 400


def get_user(username):
    try:
        found_user = User.query.get(username)
        if found_user is None:
            return {"success": False, "message": "User not found"}, 422

        return {"success": True, "data": user_schema.dump(found_user)}, 200
    except ValueError as e:
        return {"success": False,
                "message": "Error while getting user by username"}, 400


def delete_user(username):
    found_user = User.query.filter_by(username=username)

    if found_user is None:
        return {"success": False, "message": "User not found"}, 422

    found_user.delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return {"success": "False",
                "message": "Error while committing the session"}, 400

    return {"success": True, "data": "User " + str(username) + " deleted."}, 200


def get_all_tasks_for_user(username):
    try:
        user_found = User.query.get(username)
        if user_found is None:
            return {"success": False, "message": "User not found"}, 422

        json_user = user_schema.dump(user_found)

        return {"success": True, "tasks": json_user['tasks']}, 200
    except ValueError as e:
        return {"success": False,
                "message": "Error while getting all tasks for user."}


def get_all_active_tasks_for_user(username, active):
    try:
        user_found = User.query.get(username)
        if user_found is None:
            return {"success": False, "message": "User not found"}, 422

        tasks = get_all_tasks_activity(user_found, active)
        return {"success": True, "tasks": tasks}, 200

    except ValueError as e:
        return {"success": False,
                "message": "Error while getting all tasks"
                           " (active/finished) for user."}


def get_all_tasks_and_calculate_productivity(username):
    try:
        user_found = User.query.get(username)

        if user_found is None:
            return {"success": False, "message": "User not found"}, 422

        active_tasks = get_all_tasks_activity(user_found, False)
        sum_of_productivity = 0
        for task in active_tasks:
            sum_of_productivity += task["duration"]
        return {"success": True,
                "productive_time": sum_of_productivity,
                "user": user_schema.dump(user_found)}, 200
    except ValueError as e:
        return {"success": False,
                "message": "Error while trying to retrieve productivity"}, 400


def get_all_users():
    try:
        data = User.query.all()
        if data is None:
            return {"success": False,
                    "message": "No data in the database"}, 400
        data_json = users_schema.dump(data)
        return {"success": "True", "data": data_json}, 200
    except ValueError as e:
        return {"success": False,
                "message": "Error while getting all users"}


