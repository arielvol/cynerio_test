import json

from app.app_urls import URL_USER
from constants import MSG_USER_WAS_CREATED_SUCCESSFULLY, MSG_USER_ALREADY_EXISTS, MSG_USER_NAME_REQUIRED
from .base import BaseTestCase
from app.models.user import User
from app import db

class UserResourceTestCase(BaseTestCase):

    def test_get_all_users(self):

        response = self.client.get(URL_USER)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Bob')
        self.assertEqual(data[1]['name'], 'John')

    def test_post_no_user_name(self):
        response = self.client.post(URL_USER, json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], MSG_USER_NAME_REQUIRED)


    def test_post_user(self):
        user_data = {
            'name': 'Charlie'
        }

        response = self.client.post(URL_USER, data=json.dumps(user_data), content_type='application/json')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], MSG_USER_WAS_CREATED_SUCCESSFULLY.format('Charlie'))

    def test_post_existing_user(self):

        user = User(name='Dave')
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        user_data = {
            'name': 'Dave'
        }

        response = self.client.post(URL_USER, data=json.dumps(user_data), content_type='application/json')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], MSG_USER_ALREADY_EXISTS.format('Dave'))
