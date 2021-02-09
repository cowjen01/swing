import os
import pytest
from helpers import get_fixtures_path

from swing.parsers import parse_config, parse_requirements, parse_chart_definition
from swing.errors import InvalidConfigError, InvalidRequirementsError, InvalidChartDefinitionError


def test_parse_config():
    path = os.path.join(get_fixtures_path(), 'configs', 'valid.cfg')
    config = parse_config(path)

    assert config.email == 'user123@gmail.com'
    assert config.password == 'pass123'
    assert config.server_url == 'http://localhost:5000'


@pytest.mark.parametrize('filename', [
    'invalid-1.cfg',
    'invalid-2.cfg',
])
def test_invalid_config(filename):
    path = os.path.join(get_fixtures_path(), 'configs', filename)

    with pytest.raises(InvalidConfigError):
        parse_config(path)


def test_parse_requirements():
    path = os.path.join(get_fixtures_path(), 'requirements', 'valid.yaml')
    requirements = parse_requirements(path)
    
    assert len(requirements) == 2
    assert requirements[0].chart_name == 'redis'
    assert requirements[1].chart_name == 'psql'


@pytest.mark.parametrize('filename', [
    'invalid-1.yaml',
    'invalid-2.yaml',
    'invalid-3.yaml',
])
def test_invalid_requirement(filename):
    path = os.path.join(get_fixtures_path(), 'requirements', filename)

    with pytest.raises(InvalidRequirementsError):
        parse_requirements(path)


def test_parse_definition():
    path = os.path.join(get_fixtures_path(), 'definitions', 'valid.yaml')
    definition = parse_chart_definition(path)
    
    assert definition.name == 'psql'
    assert definition.version == '3.0.0'


def test_invalid_definition():
    path = os.path.join(get_fixtures_path(), 'definitions', 'invalid.yaml')

    with pytest.raises(InvalidChartDefinitionError):
        parse_chart_definition(path)
