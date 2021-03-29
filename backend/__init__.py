from flask import Flask
from .extensions import db, ma
import os
from .models.task import Task


def create_app():
    app = Flask(__name__)

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    register_extensions(app)
    register_blueprints(app)

    from .models.task import Task
    from .models.user import User

    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)


def register_blueprints(app):
    from .routes import bp
    app.register_blueprint(bp)