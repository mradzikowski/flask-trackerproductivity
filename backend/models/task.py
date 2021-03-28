from backend.extensions import db
from datetime import datetime
from marshmallow import Schema, fields


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                        nullable=False)

    def __repr__(self):
        return "<Task(task_id='%s', task_name='%s', description='%s', is_active='%s')>" \
               % (self.id, self.task_name, self.description, self.is_active)


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    task_name = fields.String()
    description = fields.String()
    is_active = fields.Boolean()
    date_created = fields.DateTime(dump_only=True)


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
