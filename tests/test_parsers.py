import os
import pytest
from helpers import get_fixtures_path

from swing.parsers import parse_config
from swing.errors import InvalidConfigError


def test_read_config():
    path = os.path.join(get_fixtures_path('configs'), 'valid.cfg')
    config = parse_config(path)

    assert config.email == 'user123@gmail.com'
    assert config.password == 'pass123'
    assert config.server_url == 'http://localhost:5000'


@pytest.mark.parametrize('filename', [
    'invalid-1.cfg',
    'invalid-2.cfg',
])
def test_invalid_config(filename):
    path = os.path.join(get_fixtures_path('configs'), filename)

    with pytest.raises(InvalidConfigError):
        parse_config(path)
