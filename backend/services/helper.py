from backend.models.user import User, user_schema


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


def get_all_tasks_activity(user, is_active):
    json_user = user_schema.dump(user)
    if is_active:
        active_tasks = []
        for task in json_user['tasks']:
            if task['is_active']:
                active_tasks.append(task)
        return active_tasks
    else:
        finished_tasks = []
        for task in json_user['tasks']:
            if not task['is_active']:
                finished_tasks.append(task)
        return finished_tasks