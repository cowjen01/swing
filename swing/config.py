import configparser
import os

from .helpers import is_valid_path
from .errors import InvalidConfigError


class Config:
    def __init__(self, server_url, email, password):
        self.server_url = server_url
        self.email = email
        self.password = password


def read_config(config_path=None):
    config = configparser.ConfigParser()

    if not config_path:
        config_path = os.path.join(os.path.expanduser('~'), '.swing')

    if not is_valid_path(config_path):
        raise InvalidConfigError('Invalid config file path')
    with open(config_path, 'r') as f:
        config.read_file(f)

    if 'swing' not in config:
        raise InvalidConfigError('Config missing swing section')

    server_url = config['swing'].get('server')
    email = config['swing'].get('email')
    password = config['swing'].get('password')

    if not server_url:
        raise InvalidConfigError('Missing server url option')

    if not email:
        raise InvalidConfigError('Missing user email option')

    if not password:
        raise InvalidConfigError('Missing user password option')

    return Config(server_url, email, password)
