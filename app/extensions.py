from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


api = Api()
bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()
mail = Mail()
moment = Moment()
