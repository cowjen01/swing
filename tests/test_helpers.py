import pytest

from swing.helpers import *
from helpers import get_fixtures_path


@pytest.mark.parametrize('url,expected', [
    ('https://docs.pytest.org/en/', True),
    ('http://localhost:5000', True),
    ('stackoverflow.com', False),
    ('creativecommons/org', False)
])
def test_validate_url(url, expected):
    assert is_valid_url(url) == expected


def test_merge():
    dict_a = {
        'a': 1,
        'b': {
            'c': 3,
            'e': 5
        }
    }
    dict_b = {
        'b': {
            'c': 1,
        }
    }
    merged_dict = merge(dict_a, dict_b)
    
    assert merged_dict['a'] is not None
    assert merged_dict['b']['c'] == 1
    assert merged_dict['b']['e'] == 5


@pytest.mark.parametrize('filename,expected', [
    ('chart', 'chart.yml'),
    ('values', 'values.yaml'),
])
def test_yaml_filename_selector(filename, expected):
    path = os.path.join(get_fixtures_path(), 'demo', 'redis')
    assert select_yaml(path, filename) == expected
