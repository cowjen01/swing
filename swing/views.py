import click
from tabulate import tabulate

from .chart import Release, Chart


def print_charts(charts: [Chart], query=None):
    if not len(charts):
        if not query:
            click.echo('No charts uploaded to the repository')
        else:
            click.echo(f'No charts found for query "{query}"')
    else:
        table = ([c.name, c.description] for c in charts)
        click.echo(tabulate(table, headers=['Name', 'Description']))
