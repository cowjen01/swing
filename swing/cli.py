import click

from .api import SwingApiService
from .config import read_config
from .errors import InvalidConfigError
from .views import print_charts


def parse_config(ctx, param, path):
    try:
        config = read_config(path)
    except InvalidConfigError:
        raise click.BadParameter('Failed to load the configuration!')
    return config


@click.group()
@click.option('-c', '--config', metavar='FILENAME', help='Swing configuration file.', callback=parse_config,
              required=False)
@click.pass_context
def swing(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj['CONFIG'] = config


@swing.command()
@click.argument('query', metavar='KEYWORD', required=False)
@click.pass_context
def search(ctx, query):
    api = SwingApiService(ctx.obj['CONFIG'].server_url)
    charts = api.list_charts(query)
    print_charts(charts)


def main():
    swing(prog_name='swing')
