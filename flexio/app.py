from flask import Flask

from flexio.blueprints.core import core
from flexio.blueprints.error_handlers import error_handlers
from flexio.extensions import debug_toolbar, csrf


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

    app.register_blueprint(core)
    app.register_blueprint(error_handlers)
    extensions(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    csrf.init_app(app)

    return None
