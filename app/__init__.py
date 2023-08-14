import os

from config import config
from flask import Flask

from app.extensions import bootstrap, db, moment, toolbar


def create_app():
    app = Flask(os.getenv('FLASK_APP') or __name__)

    # set configuration
    config_name = os.getenv('FLASK_ENV') or 'default'

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # attach extensions
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)

    # attach routes and custom error pages
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
