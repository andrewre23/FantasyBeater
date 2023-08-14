from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_praetorian import Praetorian
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy


api = Api()
bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()
mail = Mail()
moment = Moment()
praetorian = Praetorian()
toolbar = DebugToolbarExtension()
