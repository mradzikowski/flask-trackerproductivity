from backend.models.task import TaskSchema, Task
from backend.models.user import User


def get_user(username):
    try:
        found_user = User.objects.filter(username=username).first()
        return found_user
    except Exception as e:
        return {"success": False, "message": "User with provided username not found."}


