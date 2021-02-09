import pytest
import os

from swing.api import ApiService
from swing.errors import ApiHttpError
from helpers import get_fixtures_path, get_test_api


@pytest.fixture
def client(betamax_session):
    return get_test_api(betamax_session)


def test_list_charts(client: ApiService):
    charts = list(client.list_charts())

    assert len(charts) == 2
    assert charts[0].name == 'postgresql'
    assert charts[1].name == 'redis'


def test_find_chart(client: ApiService):
    charts = list(client.list_charts('redis'))

    assert len(charts) == 1
    assert charts[0].name == 'redis'
    

def test_list_releases(client: ApiService):
    releases = list(client.list_releases('redis'))

    assert len(releases) == 1
    assert releases[0].version == '1.0.0'
    

def test_list_releases_no_chart(client: ApiService):
    with pytest.raises(ApiHttpError):
        client.list_releases('nodejs')
        

def test_download_release(client: ApiService):
    zip_chart = client.download_release('redis', '1.0.0')
    
    assert zip_chart is not None
    

def test_download_release_no_version(client: ApiService):
    with pytest.raises(ApiHttpError):
        client.download_release('redis', '5.2.2')
        

def test_upload_release(client: ApiService):
    path = os.path.join(get_fixtures_path(), 'charts', 'valid.zip')
    with open(path, 'rb') as f:
        release = client.upload_release(f, 'redis', '3.0.0', 'Testing release')
        
        assert release.version == '3.0.0'
        assert release.notes == 'Testing release'


def test_upload_release_invalid_chart(client: ApiService):
    path = os.path.join(get_fixtures_path(), 'charts', 'invalid.zip')
    with open(path, 'rb') as f:
        with pytest.raises(ApiHttpError):
            client.upload_release(f, 'redis', '2.0.0')
            
            
def test_login(client: ApiService):
    user = client.login()
    
    assert user is not None
    assert user.email == 'user123@gmail.com'
