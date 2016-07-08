from datetime import timedelta
from secret import (
    DB_NAME,
    DB_ENDPOINT,
    DB_PORT,
    DB_USERNAME,
    DB_PASSWORD,
    SECRET_KEY,
    SECRET_SALT,
    MAIL_SERVER,
    MAIL_USERNAME,
    MAIL_PASSWORD
)


class Base(object):
    PROJECT_NAME = 'devit'
    SERVICE_NAME = 'Devit'

    # Server Modes
    ADMIN = False
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = \
        'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            DB_USERNAME, DB_PASSWORD, DB_ENDPOINT, DB_PORT, DB_NAME
        )

    # Session
    SECRET_SALT = SECRET_SALT
    SECRET_KEY = SECRET_KEY
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Mail
    MAIL_SERVER = MAIL_SERVER
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_PORT = 465
    MAIL_USE_SSL = True


class Dev(Base):
    # Mode
    ADMIN = True
    DEBUG = True


class Test(Base):
    # Mode
    TESTING = True

    # Database
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class Prod(Base):
    PROPAGATE_EXCEPTIONS = True
