from backend.extensions import db
from .task import Task, TaskSchema
from marshmallow import Schema, fields
from datetime import date


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(50), primary_key=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    registered = db.Column(db.DateTime, default=date.today())

    tasks = db.relationship("Task", backref="tasks", lazy=True)

    def __repr__(self):
        return "<User(username='%s', email='%s')>" \
                % (self.username, self.email)


class UserSchema(Schema):
    username = fields.String()
    email = fields.String()
    registered = fields.DateTime(dump_only=True)
    tasks = fields.List(fields.Nested(TaskSchema))


user_schema = UserSchema()
users_schema = UserSchema(many=True)