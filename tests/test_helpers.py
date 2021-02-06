import pytest

from swing.helpers import *
from helpers import get_fixtures_path


@pytest.mark.parametrize('path,expected', [
    ('foo/path/boo', False),
    (os.path.join(get_fixtures_path('configs'), 'valid.cfg'), True),
])
def test_validate_path(path, expected):
    assert is_readable_file(path) == expected


@pytest.mark.parametrize('url,expected', [
    ('https://docs.pytest.org/en/', True),
    ('http://localhost:5000', True),
    ('stackoverflow.com', False),
    ('creativecommons/org', False)
])
def test_validate_url(url, expected):
    assert is_valid_url(url) == expected
