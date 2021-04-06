from datetime import datetime, timedelta

from sqlalchemy import exc

from backend.extensions import db
from backend.models.task import Task, task_schema, tasks_schema
from backend.models.user import User
from backend.services.helper import (calculate_duration, get_tasks_last_week,
                                     get_user)


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
        return {"success": False,
                "message": "Error while creating object"}, 400


def get_task(task_id):
    try:
        found_task = Task.query.get(task_id)
        if found_task is None:
            return {"success": False, "message": "No task found"}, 422

        task_json = task_schema.dump(found_task)
        return {"success": True, "data": task_json}, 200
    except ValueError as e:
        return {"success": False,
                "message": "Error while getting a task"}, 400


def delete_task(task_id):
    found_task = User.query.get(task_id)
    if found_task is None:
        return {"success": False, "message": "No task found"}, 422

    found_task.delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return {"success": "False",
                "message": "Error while committing the session"}, 400

    return {"success": True,
            "message": "Task " + str(task_id) + " has been deleted"}, 200


def finish_task(task_id):
    try:
        found_task = Task.query.get(task_id)
        if found_task is None:
            return {"success": False, "message": "No task found"}, 422

        if found_task.is_active:
            found_task = calculate_duration(found_task)
            db.session.commit()
            return {"success": True,
                    "task": task_schema.dump(found_task)}, 200
        else:
            return {"success": True,
                    "message": "Task has been already finished"}, 200
    except ValueError as e:
        return {"success": False,
                "message": "Error while finishing the task"}


def get_all_tasks():
    try:
        data = Task.query.all()
        data_json = tasks_schema.dump(data)
        return {"success": True, "data": data_json}, 200
    except ValueError as e:
        return {"success": False,
                "message": "Error while retrieving all tasks"}


def get_tasks_from_last_week(username):
    try:
        user_found = User.query.get(username)

        if user_found is None:
            return {"success": False, "message": "No user found"}, 422

        tasks_last_week = get_tasks_last_week(user_found)

        return {"success": True,
                "tasks": tasks_schema.dump(tasks_last_week)}, 200

    except ValueError as e:
        return {"success": False,
                "message": "Error while getting tasks from last week"}, 400