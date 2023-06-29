from app import db
from flask import request
from flask_restful import Resource
from app.models.task import Task
from app.models.task_event import TaskEvent
from datetime import datetime
from constants import CHECK_OUT, MSG_TASK_ID_REQUIRED, MSG_TASK_ID_DOES_NOT_EXIST, MSG_TASK_ALREADY_CHECKED_OUT, MSG_NO_ACTIVE_TASK_EVENT, MSG_TASK_CHECKED_OUT_SUCCESSFULLY

class CheckoutResource(Resource):
    def post(self):
        task_id = request.json.get('task_id')

        if not task_id:
            return {'message': MSG_TASK_ID_REQUIRED}, 400

        task = Task.query.filter_by(id=task_id).first()

        if not task:
            return {'message': MSG_TASK_ID_DOES_NOT_EXIST.format(task_id)}, 400

        if task.status == CHECK_OUT:
            return {'message': MSG_TASK_ALREADY_CHECKED_OUT.format(task.name)}, 400
        else:
            task.status = CHECK_OUT

        active_event = TaskEvent.query.filter_by(task_id=task.id, checkout_time=None).first()
        if not active_event:
            return {'message': MSG_NO_ACTIVE_TASK_EVENT}, 400

        active_event.checkout_time = datetime.utcnow()
        db.session.commit()
        return {'message': MSG_TASK_CHECKED_OUT_SUCCESSFULLY.format(task.name)}, 200