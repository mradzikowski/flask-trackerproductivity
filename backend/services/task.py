from datetime import datetime, timedelta

from backend.extensions import db
from backend.models.task import Task, task_schema, tasks_schema
from backend.models.user import User


def get_user(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}
    if not data_json['username']:
        return {"success": False, "message": "No username provided."}
    username = data_json['username']
    return User.query.filter_by(username=username).first()


def create_task(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}, 400
    condition_for_task = (data_json['task_id'] and
                          data_json['task_name'] and data_json['username'])
    if not condition_for_task:
        return {"success": False,
                "message": "Data does not meet condition for user."}, 400
    try:
        data = task_schema.load(data_json)
        new_task = Task(**data)
        new_task.is_active = True
        new_task.date_created = datetime.now()
        new_task.duration = 0

        user = get_user(data_json)
        user.tasks.append(new_task)
        db.session.add(user)
        db.session.add(new_task)
        db.session.commit()

        return_json = task_schema.dump(data_json)

        return {"success": True, "message": return_json}, 201
    except KeyError as e:
        return {"success": False, "message": "Error while creating object"}, 400


def get_task(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}, 400
    if data_json['task_id']:
        found_task = Task.query.get(data_json['task_id'])
        if found_task:
            registered_task = task_schema.dump(found_task)
            return {"success": True, "task": registered_task}, 200
        else:
            return {"success": False,
                    "message": "Task has not been registered yet."}, 400
    else:
        return {"success": False,
                "message": f"Task - {data_json['task_id']} - "
                           f"data has not got specified task_id"}, 400


def delete_task(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}, 400
    try:
        if data_json['task_id']:
            found_task = Task.query.get(data_json['task_id'])
            if found_task is not None:
                db.session.delete(found_task)
                db.session.commit()
                return {"success": True,
                        "task": task_schema.dump(found_task),
                        "message": "Tak has been deleted."}, 200
            else:
                return {"success": False,
                        "message": "No registered task to delete."}, 400
        else:
            return {"success": False, "message": "There is no identifier."}
    except KeyError as e:
        return {"success": False,
                "message": "Error while deleting and object"}, 400


def finish_task(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}, 400
    try:
        if data_json['task_id']:
            found_task = Task.query.get(data_json['task_id'])
            if found_task is not None:
                if found_task.is_active:
                    found_task.is_active = False
                    duration = datetime.now() - found_task.date_created
                    duration = divmod(duration.total_seconds(), 60)
                    duration_rounded_two_places = round(duration[0] / 60, 2)
                    found_task.duration = duration_rounded_two_places
                    db.session.commit()
                    return {"success": True,
                            "task": task_schema.dump(found_task)}, 200
                else:
                    return {"success": False,
                            "message": "Task has been already finished"}, 400
            else:
                return {"success": False,
                        "message": "No registered task to delete."}, 400
        else:
            return {"success": False,
                    "message": "There is no identifier."}, 400
    except KeyError as e:
        return {"success": False,
                "message": "Error while deleting and object"}, 400


def get_all_tasks():
    data = Task.query.all()
    data_json = tasks_schema.dump(data)
    return {"success": True, "data": data_json}, 200


def get_tasks_from_last_week(data_json):
    if not data_json:
        return {"success": False, "message": "No data provided."}, 400
    try:
        if data_json['username']:
            found_user = User.query.get(data_json['username'])
            if found_user is not None:
                time_diff = datetime.today() - timedelta(days=7)
                tasks_user = found_user.tasks
                tasks_last_week = []
                for task in tasks_user:
                    if task.date_created >= time_diff:
                        tasks_last_week.append(task)
                return {"success": True,
                        "message": tasks_schema.dump(tasks_last_week)}, 200
            else:
                return {"success": False,
                        "message": "No registered task to delete."}, 400
        else:
            return {"success": False,
                    "message": f"User - {data_json['username']}"
                               f" - has not been registered yet."}, 400
    except ValueError as e:
        return {"success": False,
                "message": "Error while retrieving recent tasks"}, 400