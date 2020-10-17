import click

from error import _ErrorHandlingGroup
from venvs import get_entries
from venvs import create_entry
from util import format_to_table, find_format_width

_CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 200,
}


@click.command(name="list")
def _list(include_paths):
    """Lists all managed virtual environments."""
    entries = get_entries()
    if not entries:
        click.echo("No virtual environments managed with venvdir")
    rows, column_size = find_format_width(entries[0])
    table = format_to_table(rows, column_size)
    click.echo(table)


name_arg = click.argument("name")
path_option = click.option("--path", "-p", help="The format which to display the output.")


@click.command()
@name_arg
@path_option
def create(name, path):
    create_entry(name, path)


@click.group(cls=_ErrorHandlingGroup, context_settings=_CONTEXT_SETTINGS)
def cli():
    pass


cli.add_command(_list)
cli.add_command(create)
