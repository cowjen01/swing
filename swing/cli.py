import click

from .api import SwingApiService
from .config import read_config
from .errors import InvalidConfigError, ApiHttpError
from .views import print_charts


def parse_config(ctx, param, path):
    try:
        config = read_config(path)
        return config
    except InvalidConfigError as e:
        raise click.BadParameter(e.message)


@click.group()
@click.option('-c', '--config', metavar='FILENAME', help='Swing configuration file.', callback=parse_config,
              required=False)
@click.pass_context
def swing(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj['API_SERVICE'] = SwingApiService(config.server_url, config.email, config.password)


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


def main():
    swing(prog_name='swing')
