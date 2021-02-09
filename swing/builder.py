import fnmatch
import os
import subprocess
import zipfile

import yaml
from jinja2 import Environment, FileSystemLoader

from .helpers import select_yaml, merge, create_directory, remove_directory
from .parsers import parse_chart_definition
from .views import print_info, print_process


class ChartBuilder:
    def __init__(self, chart_dir):
        self.chart_dir = chart_dir
        self.install_dir = os.path.join(chart_dir, 'charts')
        self.build_dir = os.path.join(chart_dir, 'build')

    @staticmethod
    def read_values(values_dir):
        values_file = select_yaml(values_dir, 'values')
        with open(os.path.join(values_dir, values_file), 'r') as f:
            values_dict = yaml.safe_load(f)

        return values_dict

    def build_requirement(self, requirement_dir, custom_values):
        deployment_file = select_yaml(requirement_dir, 'deployment')
        
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
        for c in composes:
            args.append('-f')
            args.append(c)
        commands = ['docker-compose', *args, 'config']
        result = subprocess.run(commands, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')

    def build_chart(self, output_path):
        print_process(f'Building from \'{self.chart_dir}\'')
        create_directory(self.build_dir)
        
        files = self.list_requirement_archives(self.install_dir)
        custom_values = self.read_values(self.chart_dir)

        composes = []
        for file in files:
            requirement_name = '.'.join(file.split('.')[:-1])
            requirement_dir = os.path.join(self.install_dir, requirement_name)

            print_process(f'Building \'{requirement_name}\' requirement')

            with zipfile.ZipFile(os.path.join(self.install_dir, file), 'r') as zip_archive:
                zip_archive.extractall(requirement_dir)

            definition = parse_chart_definition(requirement_dir)
            compose = self.build_requirement(requirement_dir, custom_values)
            compose_path = os.path.join(self.build_dir, f'{definition.name}-compose.yaml')

            with open(compose_path, 'w') as f:
                f.write(compose)

            composes.append(compose_path)
            remove_directory(requirement_dir)

        print_process('Building final docker-compose file')
        docker_compose = self.merge_composes(composes)
        
        with open(output_path, 'w') as file:
            file.write(docker_compose)

        print_process('Cleaning temporary files and directories')
        remove_directory(self.build_dir)

