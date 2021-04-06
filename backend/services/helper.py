from datetime import datetime, timedelta

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


def calculate_duration(task):
    task.is_active = False
    duration = datetime.now() - task.date_created
    duration = divmod(duration.total_seconds(), 60)
    duration_rounded_two_places = round(duration[0] / 60, 2)
    task.duration = duration_rounded_two_places

    return task


def get_user(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}
    if not data_json['username']:
        return {"success": False, "message": "No username provided."}
    username = data_json['username']
    return User.query.filter_by(username=username).first()


def get_tasks_last_week(user):
    time_diff = datetime.today() - timedelta(days=7)
    tasks_user = user.tasks
    tasks_last_week = []
    for task in tasks_user:
        if task.date_created >= time_diff:
            tasks_last_week.append(task)
    return tasks_last_week