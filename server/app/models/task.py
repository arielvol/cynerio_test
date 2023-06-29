from app import db
from constants import TASK_EVENT, CHECK_OUT, TASK
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    events = db.relationship(TASK_EVENT, backref=TASK, lazy=True)
    status = db.Column(db.String(20), nullable=False, default=CHECK_OUT)