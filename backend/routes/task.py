from flask import request, jsonify
from . import bp
import backend.services.task as task_service


@bp.route('/task', methods=['POST'])
def create_task():
    try:
        data_json = request.json
        body, status = task_service.create_task(data_json)
        return jsonify(body), status
    except ValueError as e:
        return {"status": "fail", "message": "Error while creating object."}

