import requests
from base64 import b64encode

from .errors import ApiHttpError
from .chart import Chart, Release


class SwingApiService:
    def __init__(self, server_url, session=None):
        self.server_url = server_url
        self.session = session or requests.Session()

    def request(self, path, method='GET', **kwargs):
        r = self.session.request(method, f'{self.server_url}{path}', **kwargs)
        r.raise_for_status()
        return r

    def login(self, email, password):
        credentials = b64encode(bytes(f'{email}:{password}', encoding='utf-8')).decode('utf-8')
        self.request('/login', method='POST', headers={'Authorization': f'Basic {credentials}'})

    def logout(self):
        self.request('/logout', method='POST')

    def list_charts(self, query=None):
        if query:
            response = self.request('/chart', params={'query': query})
        else:
            response = self.request('/chart')

        return (Chart.from_dict(c) for c in response.json())

    def list_releases(self, chart_name, version=None):
        params = {
            'chart': chart_name
        }
        if version:
            params['version'] = version

        response = self.request('/chart', params=params)
        return (Release.from_dict(r) for r in response.json())

    def download_release(self, chart_name, version):
        filename = f'{chart_name}-{version}.zip'

        response = self.request(f'/release/{filename}')
        # open(os.path.join(dst_path, filename), 'wb').write(response.content)
        return response.content

    def upload_release(self, file):
        self.request('/release', method='POST', files=dict(chart=file))
