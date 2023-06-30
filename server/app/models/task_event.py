from app import db
from datetime import datetime

class TaskEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    checkout_time = db.Column(db.DateTime, nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    @property
    def checkin_time_iso(self):
        if self.checkin_time is not None:
            return self.checkin_time.isoformat()
        else:
            return None

    @property
    def checkout_time_iso(self):
        if self.checkout_time is not None:
            return self.checkout_time.isoformat()
        else:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'checkin_time': self.checkin_time_iso,
            'checkout_time': self.checkout_time_iso,
            'task_id': self.task_id
        }