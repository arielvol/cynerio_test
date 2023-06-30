from app import db
from flask_restful import Resource
from flask import jsonify, request
from app.models.user import User
from constants import MSG_USER_ALREADY_EXISTS, MSG_USER_NAME_REQUIRED

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({'id': user.id, 'name': user.name})
        return jsonify(user_list)

    def post(self):
        user_name = request.json.get('user_name')

        if not user_name:
            return {'message': MSG_USER_NAME_REQUIRED}, 400
        
        if User.query.filter_by(name=user_name).first():
            return {'message': MSG_USER_ALREADY_EXISTS.format(user_name)}, 400

        new_user = User(name=user_name)
        db.session.add(new_user)
        db.session.commit()
        return {"id": new_user.id, "name": new_user.name}, 201
