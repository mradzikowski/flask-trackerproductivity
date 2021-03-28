from backend.models.user import user_schema, User
from backend.extensions import db
from datetime import datetime
from backend.services.task import get_user


def create_user(data_json):
    if not data_json:
        return {"status": "failed", "message": "No data provided"}

    data = user_schema.load(data_json)
    new_user = User(**data)
    new_user.registered = datetime.now()
    db.session.add(new_user)
    db.session.commit()

    return {"status": "success", "data": user_schema.dump(new_user)}

