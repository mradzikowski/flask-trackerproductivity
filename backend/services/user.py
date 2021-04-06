import re
from datetime import datetime

from backend.extensions import db
from backend.models.user import User, user_schema, users_schema


def create_user(data_json):
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


def get_user(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}, 400
    if data_json['username']:
        found_user = User.query.get(data_json['username'])
        if found_user is not None:
            registered_user = user_schema.dump(found_user)
            return {"success": True, "user": registered_user}, 200
        return {"success": False,
                "message": f"User - {data_json['username']} - "
                           f"has not been registered yet."}


def is_registered(username):
    try:
        found_user = User.query.get(username)
        if found_user is None:
            return False
        return True
    except ValueError as e:
        return {"success": False,
                "message": "User with provided username not found."}


def is_email_registered(email):
    try:
        found_email = User.query.filter_by(email=email).first()
        if found_email is None:
            return False
        return True
    except ValueError as e:
        return {"success": False,
                "message": "User with provided email not found."}


def delete_user(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}, 400
    try:
        if is_registered(data_json['username']):
            user_to_delete = User.query.get(data_json['username'])
            db.session.delete(user_to_delete)
            db.session.commit()
            return {"success": True,
                    "message": "Successfully deleted account"}, 200
        return {"success": False,
                "message": "There is no such a user with this username"}, 400
    except ValueError as e:
        return {"success": False,
                "message": "Error while deleting the object"}, 400


def get_all_tasks_for_user(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}, 400
    try:
        if data_json['username']:
            if is_registered(data_json['username']):
                found_user = User.query.get(data_json['username'])
                if found_user is not None:
                    registered_user = user_schema.dump(found_user)
                    if registered_user["tasks"]:
                        return {"success": True,
                                "message": registered_user["tasks"]}, 200
                    return {"success": False,
                            "message": "No tasks attached to this user."}, 400
            return {"success": False,
                    "message": f"User - {data_json['username']}"
                               f" - has not been registered yet."}, 400
        return {"success": False, "message": "No data username provided."}
    except KeyError as e:
        return {"success": False,
                "message": "Error while retrieving tasks for user"}


def get_all_active_tasks_for_user(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}, 400
    try:
        if data_json['username']:
            found_user = User.query.get(data_json['username'])
            if found_user is not None:
                registered_user = user_schema.dump(found_user)
                if registered_user["tasks"]:
                    active_tasks = []
                    for task in registered_user["tasks"]:
                        if task["is_active"]:
                            active_tasks.append(task)
                    if len(active_tasks) > 0:
                        return {"success": True, "tasks": active_tasks}, 200
                    else:
                        return {"success": True, "tasks": "No tasks active"}, 200
                else:
                    return {"success": False,
                            "message": "No tasks attached to this user."}, 400
            else:
                return {"success": False,
                        "message": f"User - {data_json['username']}"
                                   f" - has not been registered yet."}, 400
        else:
            return {"success": False,
                    "message": "No data username provided."}, 400
    except ValueError as e:
        return {"success": False,
                "message": "Error while retrieving active tasks for user"}, 400


def get_all_tasks_and_calculate_productivity(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}
    try:
        if data_json['username']:
            found_user = User.query.get(data_json['username'])
            if found_user is not None:
                found_user_json = user_schema.dump(found_user)
                if found_user_json is not None:
                    if found_user_json["tasks"]:
                        finished_tasks = []
                        sum_of_productive_time = 0
                        for task in found_user_json["tasks"]:
                            if not task["is_active"]:
                                finished_tasks.append(task)
                                sum_of_productive_time += task["duration"]
                        return {"success": True,
                                "productive_time": sum_of_productive_time,
                                "user": found_user_json}, 200
                    else:
                        return {"success": True,
                                "message": "There are no finished tasks"}, 200
            else:
                return {"success": False,
                        "message": f"User - {data_json['username']}"
                                   f" - has not been registered yet."}, 400
        else:
            return {"success": False,
                    "message": "No data username provided."}, 400
    except ValueError as e:
        return {"success": False,
                "message": "Error while trying to retrieve productivity"}, 400


def get_all_users():
    data = User.query.all()
    data_json = users_schema.dump(data)
    return {"success": "True", "data": data_json}, 200


