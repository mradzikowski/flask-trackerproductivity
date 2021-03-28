from backend.extensions import db
from .task import Task


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    tasks = db.relationship("Tasks", backref="tasks", lazy=True)

    def __repr__(self):
        return "<User(user_id='%s', username='%s', email='%s')>" \
                % (self.user_id, self.username, self.email)