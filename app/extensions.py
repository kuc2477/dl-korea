from __future__ import absolute_import
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.admin import Admin
from flask.ext.marshmallow import Marshmallow
from wtforms import ValidationError
from .utils.http import error


# app db instance
db = SQLAlchemy()

# marshmallow instance
ma = Marshmallow()

# app login manager instance
login_manager = LoginManager()

# admin instance
admin = Admin()

# app mail extension instance
mail = Mail()


def configure_db(app):
    db.init_app(app)


def configure_ma(app):
    ma.init_app(app)


def configure_login(app):
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please log in to enter this page!'

    from .users.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


def configure_admin(app):
    admin.init_app(app)


def configure_mail(app):
    mail.init_app(app)


def register_error_handlers(app):
    # handles validation errors raised by decorated forms.
    # see utils/form.py for further contextual information.
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        try:
            return error(str(e), e.code)
        except AttributeError:
            return error(str(e), 400)


def register_blueprints(app, *blueprints):
    [app.register_blueprint(bp) for bp in blueprints]


def register_api_blueprints(app, *blueprints):
    [app.register_blueprint(bp, url_prefix='/api') for bp in blueprints]
