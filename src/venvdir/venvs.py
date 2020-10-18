import os
import venv
from configparser import ConfigParser

from venvdir.util import get_user_project_path


def get_entries():
    accessor = _create_accessor()
    return accessor.entries


def create_entry(name, path=None):
    if not path:
        path = _get_default_venvs_path()
    elif not os.path.exists(path):
        raise Exception("Base path '{}' does not exist.".format(path))

    env_path = os.path.join(path, name)
    if os.path.exists(env_path):
        raise Exception("Virtual environment '{}' already exists.".format(env_path))
    venv.create(env_path, with_pip=True)
    add_entry(name, path)


def add_entry(name, path):
    accessor = _create_accessor()
    accessor.create_entry(name, path)


def get_entry(name):
    accessor = _create_accessor()
    return accessor.get_entry(name)


def remove_entry(name):
    accessor = _create_accessor()
    entry = accessor.get_entry(name)
    os.remove(entry["path"])
    accessor.remove_entry(name)


def _create_accessor():
    parser = ConfigParser()
    return _EntryAccessor(parser)


def _get_default_venvs_path():
    return get_user_project_path("venvs")


class _EntryAccessor:
    DEFAULT_PATH = "."

    def __init__(self, parser):
        self.parser = parser
        file_name = "entries.cfg"
        self.path = os.path.join(get_user_project_path(), file_name)
        if not os.path.exists(self.path):
            self._save()
        else:
            self.parser.read(filenames=self.path)

    @property
    def entries(self):
        return self.parser.sections()

    def get_entry(self, name):
        try:
            entry = self.parser[name]
            return entry
        except KeyError:
            raise Exception("Entry '{}' does not exist.".format(name))

    def create_entry(self, name, path=None):
        self.parser.add_section(name)
        self.parser[name] = {}
        self.parser[name]["path"] = path or _get_default_venvs_path()
        self._save()

    def remove_entry(self, name):
        self.parser.remove_section(name)

    def _save(self):
        with open(self.path, "w+", encoding="utf-8") as file:
            self.parser.write(file)
