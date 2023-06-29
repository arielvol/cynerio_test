import json

from app.app_urls import URL_USER_TASK, URL_TASK
from .base import BaseTestCase
from constants import MSG_TASK_WAS_CREATED_SUCCESSFULLY, MSG_TASK_ALREADY_EXISTS, MSG_USER_NOT_FOUND, MSG_TASK_NAME_REQUIRED, MSG_USER_ID_REQUIRED

class TaskResourceTestCase(BaseTestCase):

    def test_get_user_not_exist(self):
        dummy_user_id = 10
        response = self.client.get(f'{URL_USER_TASK}/{dummy_user_id}')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], MSG_USER_NOT_FOUND.format(dummy_user_id))

    def test_post_no_task_name(self):
        response = self.client.post(URL_TASK, json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], MSG_TASK_NAME_REQUIRED)


    def test_post_no_user_id(self):
        task_data = {
            'name': "Task1",
        }
        response = self.client.post(URL_TASK, data=json.dumps(task_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], MSG_USER_ID_REQUIRED)


    def test_get_user_tasks(self):
        with self.app.app_context():
            #user1 = User.query.get(self.user1_id)

            response = self.client.get(f'{URL_USER_TASK}/{self.user1_id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['tasks']), 2)
            self.assertEqual(data['tasks'][0]['name'], 'Task1')
            self.assertEqual(data['tasks'][1]['name'], 'Task2')

            response = self.client.get(f'/api/task/user/{self.user2_id}')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['tasks']), 2)
            self.assertEqual(data['tasks'][0]['name'], 'Task3')
            self.assertEqual(data['tasks'][1]['name'], 'Task4')

    def test_post_task(self):

        test_task_name = 'Test Task 1'
        task_data = {
            'name': test_task_name,
            'user_id': self.user1_id
        }

        response = self.client.post(URL_TASK, data=json.dumps(task_data), content_type='application/json')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], MSG_TASK_WAS_CREATED_SUCCESSFULLY.format(test_task_name))

    def test_post_existing_task(self):

        existing_task_data = {
            'name': 'Task1',
            'user_id': self.user1_id
        }

        response = self.client.post(URL_TASK, data=json.dumps(existing_task_data), content_type='application/json')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], MSG_TASK_ALREADY_EXISTS.format(existing_task_data['name']))
