import click

from venvdir.error import _ErrorHandlingGroup
from venvdir.venvs import add_entry
from venvdir.venvs import get_entries
from venvdir.venvs import create_entry
from venvdir.venvs import get_entry
from venvdir.venvs import remove_entry
from venvdir.util import format_to_table
from venvdir.util import find_format_width

_CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 200,
}


@click.command(name="list")
def _list():
    """Lists all managed virtual environments."""
    entries = get_entries()
    if not entries:
        click.echo("Found no existing virtual environments.")
        return
    rows, column_size = find_format_width(entries)
    table = format_to_table(rows, column_size)
    click.echo(table)


name_arg = click.argument("name")


def create_path_option(required):
    return click.option(
        "--path",
        "-p",
        help="The path where to create the virtual environment. Uses ~/.venvdir/venvs/ if not given.",
        required=required,
    )


@click.command()
@name_arg
@create_path_option(False)
def create(name, path):
    """Creates a new virtual environment."""
    create_entry(name, path)


@click.command()
@name_arg
@create_path_option(True)
def add(name, path):
    """Adds an existing environment."""
    add_entry(name, path)


@click.command()
@name_arg
def remove(name):
    """Removes and deletes a virtual environments and all its files."""
    remove_entry(name)


@click.command()
@name_arg
def activate(name):
    """Activates a virtual environment for the given name."""
    entry = get_entry(name)
    activate_script_path = "{}/bin/activate".format(entry.path)
    exec(". {}".format(activate_script_path))


@click.command()
@name_arg
def which(name):
    """Shows the path to the virtual environment."""
    entry = get_entry(name)
    click.echo(entry.path)


@click.group(cls=_ErrorHandlingGroup, context_settings=_CONTEXT_SETTINGS)
def cli():
    pass


cli.add_command(_list)
cli.add_command(create)
cli.add_command(add)
cli.add_command(activate)
cli.add_command(which)
cli.add_command(remove)
