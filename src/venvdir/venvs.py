import os
import venv

from venvdir.error import VenvDirBaseError
from venvdir._configparser import config_parser
from venvdir.util import get_default_venvs_path


class ManagedVirtualEnvironment:
    def __init__(self, name, entry):
        self._name = name
        self._entry = entry

    def __getitem__(self, item):
        return self._entry[item]

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._entry["path"]

    def get(self, item):
        if item == "name":
            return self.name
        return self._entry.get(item)

    def items(self):
        items = list(self._entry.items())

        items.append(("name", self.name))

        return items

    def keys(self):
        keys = list(self._entry.keys())
        keys.append("name")
        return keys


def get_entries():
    names = config_parser.entries
    return [get_entry(name) for name in names]


def create_entry(name, path=None):
    if not path:
        path = get_default_venvs_path()
    elif not os.path.exists(path):
        raise VenvDirBaseError("Base path '{}' does not exist.".format(path))

    env_path = os.path.join(path, name)
    if os.path.exists(env_path):
        raise VenvDirBaseError("Virtual environment '{}' already exists.".format(env_path))
    venv.create(env_path, with_pip=True)
    add_entry(name, path)


def add_entry(name, path):
    config_parser.create_entry(name, path)


def get_entry(name):
    return ManagedVirtualEnvironment(name, config_parser.get_entry(name))


def remove_entry(name):
    entry = get_entry(name)
    os.remove(entry.path)
    config_parser.remove_entry(name)
