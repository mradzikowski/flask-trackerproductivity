from datetime import datetime
from backend.extensions import db
from marshmallow import Schema, fields


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime,
                             default=datetime.utcnow)
    duration = db.Column(db.Float, default=0.0)

    username = db.Column(db.String,
                         db.ForeignKey('users.username'), nullable=False)

    def __repr__(self):
        return "<Task(task_id='%s'," \
               " task_name='%s', description='%s', is_active='%s')>" \
               % (self.id, self.task_name, self.description, self.is_active)


class TaskSchema(Schema):
    task_id = fields.Integer()
    task_name = fields.String()
    description = fields.String()
    is_active = fields.Boolean()
    date_created = fields.DateTime(dump_only=True)
    duration = fields.Float()
    username = fields.String()


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
