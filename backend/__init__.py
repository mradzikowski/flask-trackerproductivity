from flask import Flask, request
from .extensions import db
import os
from .models.task import Task


def create_app():
    app = Flask(__name__)

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .models.task import Task
    from .models.user import User

    @app.route('/')
    def index():
        return {"Hello": "World"}

    return app