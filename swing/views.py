from typing import List

import click
from tabulate import tabulate

from .api import Release, Chart
from .helpers import format_date


def print_charts(charts: List[Chart], query=None):
    if not len(charts):
        if not query:
            click.echo('No charts uploaded to the repository')
        else:
            click.echo(f'No charts found for query "{query}"')
    else:
        table = ([c.name, c.description] for c in charts)
        click.echo(tabulate(table, headers=['Name', 'Description']))


def print_releases(releases: List[Release], chart_name):
    if not len(releases):
        click.echo(f'No releases found for chart "{chart_name}"')
    else:
        table = ([r.version, r.notes, format_date(r.release_date)] for r in releases)
        click.echo(tabulate(table, headers=['Version', 'Release notes', 'Published date']))


def print_error(message):
    error_label = click.style('ERROR:', fg='red')
    click.echo(f'{error_label} {message}')


def print_info(message):
    click.echo(message)
