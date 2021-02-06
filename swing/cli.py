import click
import yaml
from typing import List

from .api import ApiService
from .parsers import *
from .errors import *
from .views import print_charts
from .helpers import *


def read_config(ctx, param, path):
    try:
        config = parse_config(path)
        return config
    except InvalidConfigError as e:
        raise click.BadParameter(e.message)
    
    
def read_requirements(ctx, param, path):
    try:
        requirements = parse_requirements(path)
        return requirements
    except InvalidRequirementsError as e:
        raise click.BadParameter(e.message)


@click.group()
@click.option('-c', '--config', metavar='FILENAME', help='Configuration file', callback=read_config,
              required=False)
@click.pass_context
def swing(ctx, config: Config):
    ctx.ensure_object(dict)
    ctx.obj['API_SERVICE'] = ApiService(config.server_url, config.email, config.password)


@swing.command()
@click.argument('query', metavar='KEYWORD', required=False)
@click.pass_context
def search(ctx, query):
    api = ctx.obj['API_SERVICE']
    try:
        charts = api.list_charts(query)
        print_charts(charts, query)
    except ApiHttpError as e:
        click.echo(e.message)
        

@swing.command()
@click.option('-r', '--requirements', metavar='FILENAME', help='Dependencies file', callback=read_requirements,
              required=False)
@click.pass_context
def install(ctx, requirements: List[Requirement]):
    api: ApiService = ctx.obj['API_SERVICE']
    
    if len(requirements) == 0:
        click.echo('No requirements to install')
        return

    charts_dir = os.path.join(get_current_dir(), '.charts')
    create_directory(charts_dir)
    
    for r in requirements:
        if not r.file:
            click.echo(f'-> Downloading "{r.chart_name}" chart (version {r.version})')
            try:
                chart_path = os.path.join(charts_dir, get_archive_filename(r.chart_name, r.version))
                chart_archive = api.download_release(r.chart_name, r.version)
                with open(chart_path, 'wb') as f:
                    f.write(chart_archive)
            except ApiHttpError as e:
                click.echo(e.message)
        else:
            click.echo(f'-> Zipping "{r.chart_name}" chart from "{r.file}"')
            definition_path = get_yaml_filename(r.file, 'chart')
            
            if not definition_path:
                click.echo('Chart has no definition file')
                return
            
            with open(definition_path, 'r') as f:
                try:
                    definition_yaml = yaml.safe_load(f)
                except yaml.YAMLError:
                    click.echo('Chart has invalid definition file')

            chart_name = definition_yaml.get('name')
            version = definition_yaml.get('version')

            if not chart_name or not version:
                click.echo('Chart\'s definition has empty name or version')
                return

            chart_path = os.path.join(charts_dir, get_archive_filename(chart_name, version))
            zip_folder(r.file, chart_path)
            
            
def main():
    swing(prog_name='swing')
