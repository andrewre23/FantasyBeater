import os

from flask import Flask

from app.extensions import bootstrap, db, login, moment, toolbar
from config import config


def create_app():
    app = Flask(os.getenv('FLASK_APP') or __name__)

    # set configuration
    config_name = os.getenv('FLASK_ENV') or 'default'

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # attach extensions
    db.init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)

    login.login_view = 'auth.login'
    login.init_app(app)

    from .models.main import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # attach routes and custom error pages
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
