from backend.extensions import db
from .task import Task
from marshmallow import Schema, fields
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    registered = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)

    tasks = db.relationship("Tasks", backref="tasks", lazy=True)

    def __repr__(self):
        return "<User(user_id='%s', username='%s', email='%s')>" \
                % (self.user_id, self.username, self.email)


class UserSchema(Schema):
    user_id = fields.Integer(dump_only=True)
    username = fields.String()
    email = fields.String()
    registered = fields.DateTime(dump_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)