import os


def get_fixtures_path():
    abs_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(abs_path, 'fixtures')
