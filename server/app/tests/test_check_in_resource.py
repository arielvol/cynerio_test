from datetime import datetime
from app import db
from app.models.task import Task
from constants import CHECK_IN, CHECK_OUT, MSG_TASK_ID_REQUIRED, MSG_TASK_ID_DOES_NOT_EXIST, MSG_TASK_ALREADY_CHECKED_IN, MSG_USER_ALREADY_CHECKED_IN
from app.app_urls import URL_TASK_CHECK_IN
from app.models.task_event import TaskEvent
from .base import BaseTestCase

class CheckInResourceTestCase(BaseTestCase):

    def test_checkin_no_task_id(self):
        response = self.client.post(URL_TASK_CHECK_IN, json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], MSG_TASK_ID_REQUIRED)

    def test_checkin_task_not_found(self):
        dummy_task_id = 123
        response = self.client.post(URL_TASK_CHECK_IN, json={'task_id': dummy_task_id})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], MSG_TASK_ID_DOES_NOT_EXIST.format(dummy_task_id))

    def test_checkin_task_already_checked_in(self):
        with self.app.app_context():
            task = Task(name='Task10', user_id=self.user1_id, status=CHECK_IN)
            db.session.add(task)
            db.session.commit()

            response = self.client.post(URL_TASK_CHECK_IN, json={'task_id': task.id})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json()['message'], MSG_TASK_ALREADY_CHECKED_IN.format(task.name))

    def test_checkin_user_already_has_active_task(self):
        with self.app.app_context():
            task10 = Task(name='Task10', user_id=self.user1_id, status=CHECK_IN)
            db.session.add(task10)
            db.session.commit()

            new_event = TaskEvent(task_id=task10.id, checkin_time=datetime.now())
            db.session.add(new_event)
            db.session.commit()

            task11 = Task(name='Task11', user_id=self.user1_id, status=CHECK_OUT)
            db.session.add(task11)
            db.session.commit()

            response = self.client.post(URL_TASK_CHECK_IN, json={'task_id': task11.id})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json()['message'], MSG_USER_ALREADY_CHECKED_IN.format(task10.name))

    def test_checkin_success(self):
        with self.app.app_context():
            task = Task(name='Task10', user_id=self.user1_id, status=CHECK_OUT)
            db.session.add(task)
            db.session.commit()

            response = self.client.post(URL_TASK_CHECK_IN, json={'task_id': task.id})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['task']['name'], task.name)
