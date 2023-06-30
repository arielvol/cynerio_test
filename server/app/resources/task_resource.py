from app import db
from flask import request
from flask_restful import Resource
from app.models.user import User
from app.models.task import Task
from constants import MSG_USER_NOT_FOUND, MSG_TASK_ALREADY_EXISTS,  MSG_TASK_NAME_REQUIRED, MSG_USER_ID_REQUIRED

class TaskResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': MSG_USER_NOT_FOUND.format(user_id)}, 400

        tasks = [{"id": task.id, "name": task.name, "status": task.status} for task in user.tasks]
        return {'tasks': tasks}, 200

    def post(self):
        task_name = request.json.get('task_name')
        user_id = request.json.get('user_id')

        if not task_name:
            return {'message': MSG_TASK_NAME_REQUIRED}, 400

        if not user_id:
            return {'message': MSG_USER_ID_REQUIRED}, 400

        if Task.query.filter_by(name=task_name, user_id=user_id).first():
            return {'message': MSG_TASK_ALREADY_EXISTS.format(task_name)}, 400

        user = User.query.get(user_id)
        if not user:
            return {'message': MSG_USER_NOT_FOUND.format(user_id)}, 404

        new_task = Task(name=task_name, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()

        return {"id": new_task.id, "name": new_task.name, 'status': new_task.status}, 201
