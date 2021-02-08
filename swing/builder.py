import fnmatch
import os
import subprocess
import zipfile

import yaml
from jinja2 import Environment, FileSystemLoader

from .helpers import get_yaml_filename, merge, create_directory, remove_directory
from .parsers import parse_chart_definition


class ChartBuilder:
    def __init__(self, chart_dir):
        self.chart_dir = chart_dir
        self.install_dir = os.path.join(chart_dir, 'charts')
        self.build_dir = os.path.join(chart_dir, 'build')

    @staticmethod
    def read_values(values_dir):
        values_file = get_yaml_filename(values_dir, 'values')
        with open(os.path.join(values_dir, values_file), 'r') as f:
            values_dict = yaml.safe_load(f)

        return values_dict

    def build_requirement(self, requirement_dir, custom_values):
        deployment_file = get_yaml_filename(requirement_dir, 'deployment')
        requirement_values = self.read_values(requirement_dir)

        values = merge(requirement_values, custom_values)
        file_loader = FileSystemLoader(requirement_dir)
        env = Environment(loader=file_loader)
        template = env.get_template(deployment_file)

        return template.render(Values=values)

    @staticmethod
    def list_requirement_archives(path):
        files = []
        for file in os.listdir(path):
            if fnmatch.fnmatch(file, '*.zip'):
                files.append(file)
        return files

    @staticmethod
    def merge_composes(composes):
        args = []
        # TODO: test docker compose command
        for c in composes:
            args.append('-f')
            args.append(c)
        commands = ['docker-compose', *args, 'config']
        result = subprocess.run(commands, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')

    def build_chart(self, output_path):
        create_directory(self.build_dir)

        composes = []

        files = self.list_requirement_archives(self.install_dir)
        custom_values = self.read_values(self.chart_dir)

        for file in files:
            requirement_name = '.'.join(file.split('.')[:-1])
            requirement_dir = os.path.join(self.install_dir, requirement_name)

            with zipfile.ZipFile(os.path.join(self.install_dir, file), 'r') as zip_archive:
                zip_archive.extractall(requirement_dir)

            definition = parse_chart_definition(requirement_dir)
            compose = self.build_requirement(requirement_dir, custom_values)
            compose_path = os.path.join(self.build_dir, f'{definition.name}-compose.yaml')

            with open(compose_path, 'w') as f:
                f.write(compose)

            composes.append(compose_path)
            remove_directory(requirement_dir)

        docker_compose = self.merge_composes(composes)

        with open(output_path, 'w') as file:
            file.write(docker_compose)

        remove_directory(self.build_dir)
