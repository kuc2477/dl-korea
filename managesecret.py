#!/usr/bin/env python
from __future__ import print_function
import os
import base64
from distutils.util import strtobool
from getpass import getpass

try:
    input = raw_input
except NameError:
    pass

DEFAULT_DB_NAME = 'dl-korea'
DEFAULT_DB_USERNAME = 'postgres'
DEFAULT_MAIL_SERVER = 'smtp.gmail.com'
DEFAULT_DB_ENDPOINT = 'localhost'
DEFAULT_DB_PORT = '5432'


def ask_boolean(prompt):
    while True:
        try:
            return strtobool(input('{0} [y/n]: '.format(prompt)).lower())
        except ValueError:
            print('Please answer with y or n')


def run():
    try:
        import secret
    except ImportError:
        secret = None
        print('secret.py not found. Following process will create secret.py')

    prompt = 'Enter database name [{0}]: '.format(DEFAULT_DB_NAME)
    db_name = input(prompt) or DEFAULT_DB_NAME

    prompt = 'Enter database username [{0}]: '.format(DEFAULT_DB_USERNAME)
    db_username = input(prompt) or DEFAULT_DB_USERNAME
    db_password = getpass('Enter database password: ')

    prompt = 'Enter database endpoint [{}]: '.format(DEFAULT_DB_ENDPOINT)
    db_endpoint = input(prompt) or DEFAULT_DB_ENDPOINT

    prompt = 'Enter database port [{}]: '.format(DEFAULT_DB_PORT)
    db_port = input(prompt) or DEFAULT_DB_PORT

    if secret is None or 'SECRET_KEY' not in secret.__dict__:
        print('Secret key not found. Generating...')
        secret_key_changed = True
        secret_key = base64.b64encode(os.urandom(24)).decode()
        print('Secret key generated: {0}'.format(secret_key))
    else:
        secret_key_changed = False
        secret_key = secret.SECRET_KEY

    if secret is None or 'SECRET_SALT' not in secret.__dict__:
        print('Secret salt not found. Generating...')
        secret_salt_changed = True
        secret_salt = base64.b64encode(os.urandom(24)).decode()
        print('Secret salt generated: {0}'.format(secret_salt))
    else:
        secret_salt_changed = False
        secret_salt = secret.SECRET_SALT

    prompt = 'Enter mail server [{0}]: '.format(DEFAULT_MAIL_SERVER)
    mail_server = input(prompt) or DEFAULT_MAIL_SERVER
    mail_username = input('Enter mail username: ')
    mail_password = getpass('Enter mail password: ')

    secrets = {
        'db_name': db_name,
        'db_username': db_username,
        'db_password': db_password,
        'db_endpoint': db_endpoint,
        'db_port': db_port,
        'secret_key': secret_key,
        'secret_key_changed': 'CHANGED' if secret_key_changed else 'UNCHANGED',
        'secret_salt': secret_salt,
        'secret_salt_changed': ('CHANGED' if secret_salt_changed else
                                'UNCHANGED'),
        'mail_server': mail_server,
        'mail_username': mail_username,
        'mail_password': mail_password
    }

    prompt = '\n'.join([
        '\n',
        'Generated secrets are:\n',
        'db_name: {db_name}',
        'db username: {db_username}',
        'db password: {db_password}',
        'db endpoint: {db_endpoint}',
        'db port: {db_port}',
        'secret_key: {secret_key} ({secret_key_changed})',
        'secret_salt: {secret_salt} ({secret_salt_changed})',
        'mail_server: {mail_server}',
        'mail_username: {mail_username}',
        'mail_password: {mail_password}\n',
        'Are you sure to overwrite current secrets?',
    ]).format(**secrets)

    template = '\n'.join([
        "DB_NAME = '{db_name}'",
        "DB_USERNAME = '{db_username}'",
        "DB_ENDPOINT = '{db_endpoint}'",
        "DB_PORT = '{db_port}'",
        "DB_PASSWORD = '{db_password}'",
        "SECRET_KEY = '{secret_key}'",
        "SECRET_SALT = '{secret_salt}'",
        "MAIL_SERVER = '{mail_server}'",
        "MAIL_USERNAME = '{mail_username}'",
        "MAIL_PASSWORD = '{mail_password}'"
    ]).format(**secrets)

    if ask_boolean(prompt):
        print('\n')
        print('secret.py generated: \n')
        print(template + '\n\n')
        with open('secret.py', 'w') as f:
            f.write(template)
        print('All secrets updated!')
    else:
        print('Secrets not updated!')


if __name__ == '__main__':
    run()
