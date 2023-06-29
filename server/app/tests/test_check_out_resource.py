from datetime import datetime
from app import db
from app.models.task import Task
from constants import CHECK_IN, CHECK_OUT, MSG_TASK_ID_REQUIRED, MSG_TASK_ID_DOES_NOT_EXIST, MSG_TASK_ALREADY_CHECKED_OUT, MSG_NO_ACTIVE_TASK_EVENT, MSG_TASK_CHECKED_OUT_SUCCESSFULLY
from app.app_urls import URL_TASK_CHECK_OUT
from app.models.task_event import TaskEvent
from .base import BaseTestCase

class CheckOutResourceTestCase(BaseTestCase):

    def test_checkout_no_task_id(self):
        response = self.client.post(URL_TASK_CHECK_OUT, json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], MSG_TASK_ID_REQUIRED)

    def test_checkout_task_not_found(self):
        dummy_task_id = 123
        response = self.client.post(URL_TASK_CHECK_OUT, json={'task_id': dummy_task_id})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], MSG_TASK_ID_DOES_NOT_EXIST.format(dummy_task_id))

    def test_checkout_task_already_checked_out(self):
        with self.app.app_context():
            task = Task(name='Task10', user_id=self.user1_id, status=CHECK_OUT)
            db.session.add(task)
            db.session.commit()

            response = self.client.post(URL_TASK_CHECK_OUT, json={'task_id': task.id})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json()['message'], MSG_TASK_ALREADY_CHECKED_OUT.format(task.name))

    def test_checkout_no_active_task_event(self):
        with self.app.app_context():
            task = Task(name='Task10', user_id=self.user1_id, status=CHECK_IN)
            db.session.add(task)
            db.session.commit()

            response = self.client.post(URL_TASK_CHECK_OUT, json={'task_id': task.id})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json()['message'], MSG_NO_ACTIVE_TASK_EVENT)

    def test_checkout_success(self):
        with self.app.app_context():
            task = Task(name='Task10', user_id=self.user1_id, status=CHECK_IN)
            db.session.add(task)
            db.session.commit()

            new_event = TaskEvent(task_id=task.id, checkin_time=datetime.now())
            db.session.add(new_event)
            db.session.commit()

            response = self.client.post(URL_TASK_CHECK_OUT, json={'task_id': task.id})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['message'], MSG_TASK_CHECKED_OUT_SUCCESSFULLY.format(task.name))