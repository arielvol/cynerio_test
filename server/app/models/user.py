from app import db
from constants import TASK_MODEL, USER

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship(TASK_MODEL, backref=USER, lazy=True)