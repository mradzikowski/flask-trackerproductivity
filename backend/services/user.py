from backend.models.user import user_schema, User
from backend.extensions import db
from datetime import datetime


def create_user(data_json):
    if not data_json:
        return {"status": "failed", "message": "No data provided"}

    if is_registered(data_json['username']):
        return {"status": "fail",
                "message": "Username has been already taken"}

    if is_email_registered(data_json['email']):
        return {"status": "fail",
                "message": "Email is used in this service."}

    data = user_schema.load(data_json)
    new_user = User(**data)
    new_user.registered = datetime.now()
    db.session.add(new_user)
    db.session.commit()

    return {"status": "success", "data": user_schema.dump(new_user)}


def get_user(data_json):
    if not data_json:
        return {"status": "fail", "message": "No data provided."}
    else:
        if is_registered(data_json['username']):
            registered_user = user_schema.dump(data_json)
            return {"status": "success", "user": registered_user}
        else:
            return {"status": "fail",
                    "message": f"User - {data_json['username']} - has not been registered yet."}


def is_registered(username):
    try:
        found_user = User.query.get(username)
        if found_user is None:
            return False
        else:
            return True
    except ValueError as e:
        return {"success": False, "message": "User with provided username not found."}


def is_email_registered(email):
    try:
        found_email = User.query.filter_by(email=email).first()
        if found_email is None:
            return False
        else:
            return True
    except ValueError as e:
        return {"success": False, "message": "User with provided email not found."}


def delete_user(data_json):
    if not data_json:
        return {"status": "fail", "message": "No data provided."}
    else:
        try:
            if is_registered(data_json['username']):
                user_to_delete = User.query.get(data_json['username'])
                db.session.delete(user_to_delete)
                db.session.commit()
                return {"status": "success", "message": "Successfully deleted account"}
            else:
                return {"status": "fail", "message": "There is no such a user with this username"}

        except ValueError as e:
            return {"status": "fail", "message": "Error while deleting the object"}