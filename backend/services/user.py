from backend.models.user import user_schema, User
from backend.extensions import db
from datetime import datetime


def create_user(data_json):
    if not data_json:
        return {"status": "failed", "message": "No data provided"}, 400

    if is_registered(data_json['username']):
        return {"status": "fail",
                "message": "Username has been already taken"}, 400

    if is_email_registered(data_json['email']):
        return {"status": "fail",
                "message": "Email is used in this service."}, 400

    data = user_schema.load(data_json)
    new_user = User(**data)
    new_user.registered = datetime.now()
    db.session.add(new_user)
    db.session.commit()

    return {"status": "success", "data": user_schema.dump(new_user)}, 201


def get_user(data_json):
    if not data_json:
        return {"status": "fail", "message": "No data provided."}, 400
    else:
        if data_json['username']:
            found_user = User.query.get(data_json['username'])
            if found_user is not None:
                registered_user = user_schema.dump(found_user)
                return {"status": "success", "user": registered_user}, 200
            else:
                return {"status": "fail",
                        "message": f"User - {data_json['username']} - "
                                   f"has not been registered yet."}


def is_registered(username):
    try:
        found_user = User.query.get(username)
        if found_user is None:
            return False
        else:
            return True
    except ValueError as e:
        return {"success": False,
                "message": "User with provided username not found."}


def is_email_registered(email):
    try:
        found_email = User.query.filter_by(email=email).first()
        if found_email is None:
            return False
        else:
            return True
    except ValueError as e:
        return {"success": False,
                "message": "User with provided email not found."}


def delete_user(data_json):
    if not data_json:
        return {"status": "fail", "message": "No data provided."}, 400
    else:
        try:
            if is_registered(data_json['username']):
                user_to_delete = User.query.get(data_json['username'])
                db.session.delete(user_to_delete)
                db.session.commit()
                return {"status": "success",
                        "message": "Successfully deleted account"}, 200
            else:
                return {"status": "fail",
                        "message": "There is no such a user with this username"}, 400
        except ValueError as e:
            return {"status": "fail", "message": "Error while deleting the object"}, 400


def get_all_tasks_for_user(data_json):
    if not data_json:
        return {"status": "fail", "message": "No data provided."}, 400
    else:
        try:
            if data_json['username']:
                if is_registered(data_json['username']):
                    found_user = User.query.get(data_json['username'])
                    if found_user is not None:
                        registered_user = user_schema.dump(found_user)
                        if registered_user["tasks"]:
                            return {"status": "success",
                                    "message": registered_user["tasks"]}, 200
                        else:
                            return {"status": "fail",
                                    "message": "No tasks attached to this user."}, 400
                else:
                    return {"status": "fail",
                            "message": f"User - {data_json['username']}"
                                       f" - has not been registered yet."}, 400
            else:
                return {"status": "fail", "message": "No data username provided."}
        except KeyError as e:
            return {"status": "fail",
                    "message": "Error while retrieving tasks for user"}


def get_all_active_tasks_for_user(data_json):
    if not data_json:
        return {"status": "fail", "message": "No data provided."}, 400
    else:
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
                            return {"status": "success", "message": active_tasks}, 200
                        else:
                            return {"message", active_tasks}, 200
                    else:
                        return {"status": "fail",
                                "message": "No tasks attached to this user."}, 400
                else:
                    return {"status": "fail",
                            "message": f"User - {data_json['username']}"
                                       f" - has not been registered yet."}, 400
            else:
                return {"status": "fail",
                        "message": "No data username provided."}, 400
        except ValueError as e:
            return {"status": "fail",
                    "message": "Error while retrieving active tasks for user"}, 400