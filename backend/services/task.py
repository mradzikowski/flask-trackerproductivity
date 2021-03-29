from backend.models.task import task_schema, Task
from backend.models.user import User
from datetime import datetime
from backend.extensions import db


def get_user(data_json):
    if not data_json:
        return {"status": "fail", "message": "No data provided."}
    if not data_json['username']:
        return {"status": "fail", "message": "No username provided."}
    username = data_json['username']
    return User.query.filter_by(username=username).first()


def create_task(data_json):
    if not data_json:
        return {"status": "fail", "message": "No data provided."}
    condition_for_task = (data_json['task_id'] and
                          data_json['task_name'] and data_json['username'])
    if not condition_for_task:
        return {"status": "fail", "message": "Data does not meet condition for user."}
    try:
        data = task_schema.load(data_json)
        new_task = Task(**data)
        new_task.is_active = True
        new_task.date_created = datetime.now()

        user = get_user(data_json)
        user.tasks.append(new_task)
        db.session.add(user)
        db.session.add(new_task)
        db.session.commit()

        return_json = task_schema.dump(data_json)

        return {"status": "success", "message": return_json}, 201
    except ValueError as e:
        return {"status": "fail", "message": "Error while creating object"}


def get_task(data_json):
    if not data_json:
        return {"status": "fail", "message": "No data provided."}, 400
    else:
        if data_json['task_id']:
            found_task = Task.query.get(data_json['task_id'])
            if found_task:
                registered_task = task_schema.dump(found_task)
                return {"status": "success", "task": registered_task}, 200
            else:
                return {"status": "fail", "message": "Task has not been registered yet."}, 400
        else:
            return {"status": "fail",
                    "message": f"Task - {data_json['task_id']} - data has not got specified task_id"}, 400




