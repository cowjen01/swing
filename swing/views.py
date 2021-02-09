from typing import List

import click
from tabulate import tabulate

from .api import Release, Chart
from .helpers import format_date


def print_error(message):
    error_label = click.style('ERROR', fg='red')
    click.echo(f'{error_label}: {message}')


def print_warning(message):
    warn_label = click.style('WARNING', fg='yellow')
    click.echo(f'{warn_label}: {message}')
    
    
def print_ok(message):
    ok_label = click.style('SUCCESS', fg='green')
    click.echo(f'{ok_label}: {message}')


def print_info(message):
    click.echo(message)
    

def print_process(message):
    print_info(f'   -> {message}')


def print_charts(charts: List[Chart], query=None):
    if not len(charts):
        if not query:
            print_warning('No charts uploaded to the repository')
        else:
            print_warning(f'No charts found for query "{query}"')
    else:
        table = ([c.name, c.description] for c in charts)
        print_info(tabulate(table, headers=['Name', 'Description']))


def print_releases(releases: List[Release], chart_name):
    if not len(releases):
        print_warning(f'No releases found for chart "{chart_name}"')
    else:
        table = ([r.version, r.notes, format_date(r.release_date)] for r in releases)
        print_info(tabulate(table, headers=['Version', 'Release notes', 'Published date']))

