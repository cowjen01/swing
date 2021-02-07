import os
from typing import List

import click

from .api import ApiService
from .chart import get_archive_filename, zip_chart_folder
from .errors import InvalidChartDefinitionError, InvalidRequirementsError, InvalidConfigError, ApiHttpError
from .helpers import get_current_dir, create_directory
from .parsers import parse_config, parse_requirements, parse_chart_definition, Config, Requirement
from .views import print_charts, print_releases


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


def read_chart_path(ctx, param, path):
    if not path:
        path = get_current_dir()
    if not is_readable_dir(path):
        raise click.BadParameter('Invalid chart path')
    return path


@click.group()
@click.option('-c', '--config', metavar='FILENAME', help='Swing configuration file.', callback=read_config,
              required=False)
@click.pass_context
def swing(ctx, config: Config):
    """Client for communicating with the remote respository."""
    ctx.ensure_object(dict)
    ctx.obj['API_SERVICE'] = ApiService(config.server_url, config.email, config.password)


@swing.command()
@click.argument('query', metavar='KEYWORD', required=False)
@click.pass_context
def search(ctx, query):
    """Search for available charts."""
    api = ctx.obj['API_SERVICE']
    try:
        charts = api.list_charts(query)
        print_charts(charts, query)
    except ApiHttpError as e:
        click.echo(e.message)


@swing.command()
@click.argument('chart_name', metavar='CHART', required=True)
@click.pass_context
def show(ctx, chart_name):
    """Show releases of specific chart."""
    api: ApiService = ctx.obj['API_SERVICE']
    try:
        charts = api.list_releases(chart_name)
        print_releases(charts, chart_name)
    except ApiHttpError as e:
        click.echo(e.message)


@swing.command()
@click.option('-r', '--requirements', metavar='FILENAME', help='Chart dependencies file.', callback=read_requirements,
              required=False)
@click.pass_context
def install(ctx, requirements: List[Requirement]):
    """Install requirements specified in the dependency file."""
    api: ApiService = ctx.obj['API_SERVICE']
    charts_dir = os.path.join(get_current_dir(), '.charts')

    if len(requirements) == 0:
        click.echo('No requirements to install')
        return

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
            try:
                definition = parse_chart_definition(r.file)
                chart_path = os.path.join(charts_dir, get_archive_filename(definition.name, definition.version))

                click.echo(f'-> Zipping "{definition.name}" chart from "{r.file}" (version {definition.version})')

                archive = zip_chart_folder(r.file)
                with open(chart_path, 'wb') as f:
                    f.write(archive.getbuffer())
                archive.close()
            except InvalidChartDefinitionError as e:
                click.echo(e.message)


@swing.command()
@click.argument('path', metavar='PATH', required=False, callback=read_chart_path)
@click.option('-n', '--notes', metavar='MESSAGE', help='Release notes.', required=False)
@click.pass_context
def publish(ctx, path, notes):
    """Upload local chart to the remote respository."""
    api: ApiService = ctx.obj['API_SERVICE']

    try:
        definition = parse_chart_definition(path)
        archive = zip_chart_folder(path)

        release = api.upload_release(archive.getbuffer(), definition.name, definition.version, notes)
        click.echo(f'Release published: {release.archive_url}')
    except ApiHttpError as e:
        click.echo(e.message)
    except InvalidChartDefinitionError as e:
        click.echo(e.message)


@swing.command()
@click.argument('chart_name', metavar='CHART', required=True)
@click.option('-v', '--version', metavar='VERSION', help='Version of release to delete.', required=False)
@click.pass_context
def delete(ctx, chart_name, version):
    """Delete chart or specific release from repository server."""
    api: ApiService = ctx.obj['API_SERVICE']

    try:
        api.delete_chart(chart_name, version)
        if version:
            click.echo(f'Release with version {version} was deleted')
        else:
            click.echo(f'Chart {chart_name} was deleted')
    except ApiHttpError as e:
        click.echo(e.message)


def main():
    swing(prog_name='swing')
