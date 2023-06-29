from app import db
from app.app_urls import URL_TASK_REPORT
from app.models.task_event import TaskEvent
from constants import MSG_NO_TASKS_TO_REPORT
from .base import BaseTestCase
from datetime import datetime, timedelta

class TaskReportResourceTestCase(BaseTestCase):

    def test_get_tasks_report_no_tasks(self):
        response = self.client.get(URL_TASK_REPORT)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], MSG_NO_TASKS_TO_REPORT)

    def test_get_tasks_report(self):
        with self.app.app_context():

            task_event1 = TaskEvent(task_id=self.task1_id, checkin_time=datetime.now(), checkout_time=datetime.now()+timedelta(hours=2))
            task_event2 = TaskEvent(task_id=self.task2_id, checkin_time=datetime.now(), checkout_time=datetime.now()+timedelta(hours=3))

            db.session.add(task_event1)
            db.session.add(task_event2)
            db.session.commit()

        response = self.client.get(URL_TASK_REPORT)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['Bob']['Task1']['hours'], 2)
        self.assertEqual(data['Bob']['Task2']['hours'], 3)