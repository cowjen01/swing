import os
import betamax

from swing.api import ApiService


def get_fixtures_path():
    abs_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(abs_path, 'fixtures')


with betamax.Betamax.configure() as config:
    config.cassette_library_dir = os.path.join(get_fixtures_path(), 'cassettes')


def get_test_api(betamax_session):
    return ApiService(
        email='user123@gmail.com',
        password='pass123',
        server_url='http://localhost:5000',
        session=betamax_session
    )
