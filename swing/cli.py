import click

from .api import ApiService
from .core import SwingCore
from .errors import InvalidChartDefinitionError, InvalidRequirementsError, InvalidConfigError, ApiHttpError, SwingCoreError
from .parsers import parse_config, parse_requirements, Config
from .views import print_error


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


class CatchAllExceptions(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except ApiHttpError as e:
            print_error(e.message)
        except InvalidChartDefinitionError as e:
            print_error(e.message)
        except SwingCoreError as e:
            print_error(e.message)


@click.group(cls=CatchAllExceptions)
@click.option('-c', '--config', metavar='FILENAME', help='Swing configuration file.', callback=read_config,
              required=False, type=click.Path(exists=True))
@click.pass_context
def swing(ctx, config: Config):
    """Client for communication with the remote respository."""
    ctx.ensure_object(dict)
    api_service = ApiService(config.server_url, config.email, config.password)
    ctx.obj['SWING_CORE'] = SwingCore(api_service)


@swing.command()
@click.argument('query', metavar='KEYWORD', required=False)
@click.pass_context
def search(ctx, query):
    """Search for available charts."""
    core: SwingCore = ctx.obj['SWING_CORE']
    core.list_charts(query)


@swing.command()
@click.argument('chart_name', metavar='CHART', required=True)
@click.pass_context
def show(ctx, chart_name):
    """Show releases of the specific chart."""
    core: SwingCore = ctx.obj['SWING_CORE']
    core.list_releases(chart_name)


@swing.command()
@click.option('-r', '--requirements', metavar='FILENAME', help='Chart dependencies file.', callback=read_requirements,
              required=False, type=click.Path(exists=True))
@click.pass_context
def install(ctx, requirements):
    """Install requirements specified in the dependency file."""
    core: SwingCore = ctx.obj['SWING_CORE']
    core.install_requirements(requirements)


@swing.command()
@click.argument('chart_path', metavar='PATH', required=False, type=click.Path(exists=True))
@click.option('-n', '--notes', metavar='MESSAGE', help='Some release notes.', required=False)
@click.pass_context
def publish(ctx, chart_path, notes):
    """Upload the local chart to the remote respository."""
    core: SwingCore = ctx.obj['SWING_CORE']
    core.publish_release(chart_path, notes)


@swing.command()
@click.argument('chart_name', metavar='CHART', required=True)
@click.option('-v', '--version', metavar='VERSION', help='Version of the release to delete.', required=False)
@click.pass_context
def delete(ctx, chart_name, version):
    """Deletethe  chart or specific release from the repository server."""
    core: SwingCore = ctx.obj['SWING_CORE']
    core.delete_chart(chart_name, version)


@swing.command()
@click.argument('chart_path', metavar='PATH', required=False, type=click.Path(exists=True))
@click.option('-o', '--output', metavar='PATH', help='Docker compose output path.', required=False)
@click.pass_context
def build(ctx, chart_path, output):
    """Build the installed charts to the final docker compose file."""
    core: SwingCore = ctx.obj['SWING_CORE']
    core.build_chart(chart_path, output)


def main():
    swing(prog_name='swing')
