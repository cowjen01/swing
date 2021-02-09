import os
import zipfile
from io import BytesIO

from .builder import ChartBuilder
from .helpers import get_current_dir, create_directory, get_archive_filename, is_tool, select_yaml
from .parsers import parse_chart_definition
from .views import print_charts, print_releases, print_ok, print_process
from .errors import SwingCoreError


class SwingCore:
    def __init__(self, api):
        self.api = api

    def list_charts(self, query):
        charts = self.api.list_charts(query)
        print_charts(charts, query)

    def list_releases(self, chart_name):
        charts = self.api.list_releases(chart_name)
        print_releases(charts, chart_name)
    
    @staticmethod
    def zip_folder(dir_path):
        archive = BytesIO()
        with zipfile.ZipFile(archive, 'w') as zip_archive:
            relroot = os.path.abspath(os.path.join(dir_path))
            for dirname, subdirs, files in os.walk(dir_path):
                for file in files:
                    filename = os.path.join(dirname, file)
                    arcname = os.path.join(os.path.relpath(dirname, relroot), file)
                    zip_archive.write(filename, arcname=arcname)
        return archive

    def download_requirement(self, requirement, install_dir):
        chart_name = requirement.chart_name
        version = requirement.version

        print_process(f'Downloading \'{chart_name}-{version}\'')

        chart_path = os.path.join(install_dir, get_archive_filename(chart_name, version))
        chart_archive = self.api.download_release(chart_name, version)

        with open(chart_path, 'wb') as f:
            f.write(chart_archive)

    def pack_requirement(self, requirement, install_dir):
        filename = select_yaml(requirement.file, 'chart')
        definition_path = os.path.join(requirement.file, filename)
        definition = parse_chart_definition(definition_path)
        chart_path = os.path.join(install_dir, get_archive_filename(definition.name, definition.version))

        print_process(f'Packing \'{definition.chart_name}-{definition.version}\' from \'{requirement.file}\'')

        archive = self.zip_folder(requirement.file)
        with open(chart_path, 'wb') as f:
            f.write(archive.getbuffer())

    def install_requirements(self, requirements):
        install_dir = os.path.join(get_current_dir(), 'charts')

        if len(requirements) == 0:
            raise SwingCoreError('No requirements to install.')

        print_process(f'Installing {len(requirements)} requirements')
        create_directory(install_dir)

        for r in requirements:
            if not r.file:
                self.download_requirement(r, install_dir)
            else:
                self.pack_requirement(r, install_dir)
                
        print_ok('All requirements are installed.')

    def publish_release(self, chart_dir, notes):
        if not chart_dir:
            chart_dir = get_current_dir()
            
        filename = select_yaml(chart_dir, 'chart')
        definition_path = os.path.join(chart_dir, filename)
        definition = parse_chart_definition(definition_path)
        archive = self.zip_folder(chart_dir)

        release = self.api.upload_release(archive.getbuffer(), definition.name, definition.version, notes)
        print_ok(f'The release is published at {release.archive_url}.')

    def delete_chart(self, chart_name, version):
        self.api.delete_chart(chart_name, version)
        if version:
            print_ok(f'The release {version} of the \'{chart_name}\' chart is deleted.')
        else:
            print_ok(f'The \'{chart_name}\' chart is deleted.')

    def build_chart(self, chart_dir, output_path):
        if not is_tool('docker-compose'):
            raise SwingCoreError('To build the chart, the docker-compose command has to be installed.')

        if not chart_dir:
            chart_dir = get_current_dir()

        if not output_path:
            output_path = os.path.join(chart_dir, 'docker-stack.yaml')

        builder = ChartBuilder(chart_dir)
        builder.build_chart(output_path)
        
        print_ok(f'The chart is built at \'{output_path}\'.')
