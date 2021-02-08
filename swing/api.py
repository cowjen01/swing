from base64 import b64encode

import requests

from .errors import ApiHttpError
from .helpers import get_archive_filename


class Chart:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def from_dict(cls, json):
        name = json.get('name')
        description = json.get('description')
        return cls(name, description)


class Release:
    def __init__(self, version, release_date, archive_url, notes):
        self.version = version
        self.release_date = release_date
        self.archive_url = archive_url
        self.notes = notes

    @classmethod
    def from_dict(cls, json):
        version = json.get('version')
        release_date = json.get('releaseDate')
        archive_url = json.get('archiveUrl')
        notes = json.get('notes')
        return cls(version, release_date, archive_url, notes)


class ApiService:
    def __init__(self, server_url, email, password, session=None):
        self.server_url = server_url
        self.email = email
        self.password = password
        self.session = session or requests.Session()

    @staticmethod
    def parse_error_response(response):
        error = response.json()
        return error.get('description'), error.get('code')

    def request(self, path, method='GET', **kwargs):
        response = None
        try:
            response = self.session.request(method, f'{self.server_url}{path}', **kwargs)
            response.raise_for_status()
            return response
        except requests.ConnectionError:
            raise ApiHttpError('Repository server is not available')
        except requests.HTTPError:
            message, code = self.parse_error_response(response)
            raise ApiHttpError(message, code)

    def login(self):
        credentials = b64encode(bytes(f'{self.email}:{self.password}', encoding='utf-8')).decode('utf-8')
        self.request('/login', method='POST', headers={'Authorization': f'Basic {credentials}'})

    def logout(self):
        self.request('/logout', method='POST')

    def list_charts(self, query=None):
        if query:
            response = self.request('/chart', params={'query': query})
        else:
            response = self.request('/chart')

        return [Chart.from_dict(c) for c in response.json()]

    def list_releases(self, chart_name, version=None):
        params = {
            'chart': chart_name
        }
        if version:
            params['version'] = version

        response = self.request('/release', params=params)

        return [Release.from_dict(r) for r in response.json()]

    def download_release(self, chart_name, version):
        filename = get_archive_filename(chart_name, version)
        response = self.request(f'/release/{filename}')

        return response.content

    def upload_release(self, archive_file, chart_name, version, notes=None):
        self.login()

        filename = get_archive_filename(chart_name, version)
        files = dict(
            chart=(filename, archive_file),
            notes=notes
        )

        data = dict()
        if notes:
            data['notes'] = notes

        response = self.request('/release', method='POST', files=files, data=data)
        return Release.from_dict(response.json())

    def delete_chart(self, chart_name, version=None):
        self.login()

        params = dict()
        if version:
            params['version'] = version

        self.request(f'/chart/{chart_name}', method='DELETE', params=params)
