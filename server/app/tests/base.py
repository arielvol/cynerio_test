import unittest
from app import create_app, db
from app.models.user import User
from app.models.task import Task
from config import config
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from constants import CHECK_OUT

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        test_uri = f"postgresql://{config.get('PGUSER')}:{config.get('PGPASSWORD')}@{config.get('PGHOST')}:{config.get('PGPORT')}/test_db"
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': test_uri
        })
        engine = create_engine(test_uri)

        if not database_exists(engine.url):
            create_database(engine.url)

        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user1 = User(name='Bob')
            user2 = User(name='John')
            db.session.add_all([user1, user2])
            db.session.commit()
            task1 = Task(name='Task1', user_id=user1.id, status=CHECK_OUT)
            task2 = Task(name='Task2', user_id=user1.id, status=CHECK_OUT)
            task3 = Task(name='Task3', user_id=user2.id, status=CHECK_OUT)
            task4 = Task(name='Task4', user_id=user2.id, status=CHECK_OUT)
            db.session.add_all([task1, task2, task3, task4])
            db.session.commit()

            self.user1_id = user1.id
            self.user2_id = user2.id
            self.task1_id = task1.id
            self.task2_id = task2.id
            self.task3_id = task3.id
            self.task4_id = task4.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()