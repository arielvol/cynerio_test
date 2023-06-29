from app import db
from datetime import datetime

class TaskEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    checkout_time = db.Column(db.DateTime, nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)