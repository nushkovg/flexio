from flask import Flask
from celery import Celery
from itsdangerous import URLSafeTimedSerializer

from flexio.blueprints.admin import admin
from flexio.blueprints.core import core
from flexio.blueprints.contact import contact
from flexio.blueprints.error_handlers import error_handlers
from flexio.blueprints.user import user
from flexio.blueprints.units import units
from flexio.blueprints.user.models import User
from flexio.extensions import (
    debug_toolbar,
    mail,
    csrf,
    db,
    login_manager
)

CELERY_TASK_LIST = [
    'flexio.blueprints.contact.tasks',
    'flexio.blueprints.user.tasks'
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(settings_override=None):
    """
    Creates the Flexio Flask application. Uses an external settings file.

    :return: Flexio Flask Application
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(admin)
    app.register_blueprint(core)
    app.register_blueprint(error_handlers)
    app.register_blueprint(contact)
    app.register_blueprint(user)
    app.register_blueprint(units)
    extensions(app)
    authentication(app, User)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return None


def authentication(app, user_model):
    """
    Initialize the Flask-Login extension (mutates the app passed in).

    :param app: Flask application instance
    :param user_model: Model that contains the authentication information
    :type user_model: SQLAlchemy model
    :return: None
    """
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)

    @login_manager.token_loader
    def load_token(token):
        duration = app.config['REMEMBER_COOKIE_DURATION'].total_seconds()
        serializer = URLSafeTimedSerializer(app.secret_key)

        data = serializer.loads(token, max_age=duration)
        user_uid = data[0]

        return user_model.query.get(user_uid)
