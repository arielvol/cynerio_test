from app import db
from flask import request, jsonify
from flask_restful import Resource
from app.models.task import Task
from app.models.user import User
from app.models.task_event import TaskEvent
from constants import CHECK_IN, MSG_TASK_ID_REQUIRED, MSG_TASK_ID_DOES_NOT_EXIST, MSG_TASK_ALREADY_CHECKED_IN, MSG_USER_ALREADY_CHECKED_IN

class CheckInResource(Resource):
    def post(self):
        task_id = request.json.get('task_id')

        if not task_id:
            return {'message': MSG_TASK_ID_REQUIRED}, 400

        task = Task.query.filter_by(id=task_id).first()

        if not task:
            return {'message': MSG_TASK_ID_DOES_NOT_EXIST.format(task_id)}, 400

        if task.status == CHECK_IN:
            return {'message': MSG_TASK_ALREADY_CHECKED_IN.format(task.name)}, 400
        else:
            task.status = CHECK_IN

        user = User.query.filter_by(id=task.user_id).first()

        # check if user has any active task
        active_task = Task.query.join(TaskEvent).filter(Task.user_id==user.id, Task.status==CHECK_IN, TaskEvent.checkout_time==None).first()
        if active_task:
            return {'message': MSG_USER_ALREADY_CHECKED_IN.format(active_task.name)}, 400


        new_event = TaskEvent(task_id=task.id)
        db.session.add(new_event)
        db.session.commit()
        return { "task": {"id": task.id, "name": task.name, "status": task.status} , "task_event": new_event.to_dict()}, 200
