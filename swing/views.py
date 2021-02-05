import click
from tabulate import tabulate

from .chart import Release, Chart


def print_charts(charts: [Chart]):
    table = ([c.name, c.description] for c in charts)
    print(tabulate(table, headers=['Name', 'Description']))
