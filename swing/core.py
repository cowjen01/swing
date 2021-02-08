import os

from .builder import ChartBuilder
from .helpers import get_current_dir, create_directory, get_archive_filename, zip_chart_folder
from .parsers import parse_chart_definition
from .views import print_charts, print_releases, print_info


class SwingCore:
    def __init__(self, api):
        self.api = api

    def list_charts(self, query):
        charts = self.api.list_charts(query)
        print_charts(charts, query)

    def list_releases(self, chart_name):
        charts = self.api.list_releases(chart_name)
        print_releases(charts, chart_name)

    def download_requirement(self, requirement, install_dir):
        chart_name = requirement.chart_name
        version = requirement.version

        print_info(f'-> Downloading "{chart_name}" chart (version {version})')

        chart_path = os.path.join(install_dir, get_archive_filename(chart_name, version))
        chart_archive = self.api.download_release(chart_name, version)

        with open(chart_path, 'wb') as f:
            f.write(chart_archive)

    def pack_requirement(self, requirement, install_dir):
        definition = parse_chart_definition(requirement.file)
        chart_path = os.path.join(install_dir, get_archive_filename(definition.name, definition.version))

        print_info(f'-> Zipping "{definition.name}" chart from "{requirement.file}" (version {definition.version})')

        archive = zip_chart_folder(requirement.file)
        with open(chart_path, 'wb') as f:
            f.write(archive.getbuffer())

    def install_requirements(self, requirements):
        install_dir = os.path.join(get_current_dir(), 'charts')

        if len(requirements) == 0:
            print_info('No requirements to install')
            return

        create_directory(install_dir)

        for r in requirements:
            if not r.file:
                self.download_requirement(r, install_dir)
            else:
                self.pack_requirement(r, install_dir)

    def publish_release(self, chart_dir, notes):
        definition = parse_chart_definition(chart_dir)
        archive = zip_chart_folder(chart_dir)

        release = self.api.upload_release(archive.getbuffer(), definition.name, definition.version, notes)
        print_info(f'Release published: {release.archive_url}')

    def delete_chart(self, chart_name, version):
        self.api.delete_chart(chart_name, version)
        if version:
            print_info(f'Release with version {version} was deleted')
        else:
            print_info(f'Chart {chart_name} was deleted')

    def build_chart(self, chart_dir, output_path):
        if not chart_dir:
            chart_dir = get_current_dir()

        if not output_path:
            output_path = os.path.join(chart_dir, 'docker-stack.yaml')

        builder = ChartBuilder(chart_dir)
        builder.build_chart(output_path)
