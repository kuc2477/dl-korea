import os
import config
from flask import Flask
from flask_cors import CORS
from .extensions import (
    configure_db,
    configure_ma,
    configure_admin,
    configure_mail,
    configure_login,
    register_blueprints,
    register_api_blueprints,
    register_error_handlers,
)
from .users.views import bp as users_bp
from .plans.views import bp as plans_bp
from .main.views import bp as main_bp


def get_config(cfg):
    if isinstance(cfg, str):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg


def create_app(cfg):
    # configure app from the config
    config = get_config(cfg)
    app = Flask(config.PROJECT_NAME)
    app.config.from_object(config)

    # configure flask extensions
    configure_db(app)
    configure_ma(app)
    configure_login(app)
    configure_mail(app)

    if config.ADMIN:
        configure_admin(app)

    if config.DEBUG:
        CORS(app)

    # register blueprints and error handlers
    register_blueprints(app, main_bp)
    register_api_blueprints(app, users_bp, plans_bp)
    register_error_handlers(app)
    return app


def create_app_from_env():
    try:
        config_name = os.environ['DEVIT_CONFIG'].title()
    except KeyError:
        config_name = 'Dev'
    return create_app(getattr(config, config_name))
