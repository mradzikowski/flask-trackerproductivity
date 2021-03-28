from backend.extensions import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)

    def __repr__(self):
        return "<Task(id='%s', task_name='%s', description='%s', is_active='%s')>" \
               % (self.id, self.task_name, self.description, self.is_active)
