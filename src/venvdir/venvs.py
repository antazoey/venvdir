import os
from venv import create as create_venv
from os.path import exists as does_path_exist

from venvdir.error import VenvDirBaseError
from venvdir._configparser import config_parser
from venvdir.util import get_default_venvs_path
from venvdir.util import remove_directory


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
        if item.lower() == "name":
            return self.name
        return self._entry.get(item)

    def items(self):
        items = list(self._entry.items())
        if len(items):
            items.append(("name", self.name))
        return items

    def keys(self):
        keys = list(self._entry.keys())
        if len(keys):
            keys.append("name")
        return keys

    def __repr__(self):
        return "Virtual Env: (name={}, path={})".format(self.name, self.path)

    def __str__(self):
        return "Virtual Env: (name={}, path={})".format(self.name, self.path)


def get_entries():
    names = config_parser.entries
    return [get_entry(name) for name in names]


def create_entry(name, path=None):
    if not path:
        path = get_default_venvs_path()
    elif not does_path_exist(path):
        raise VenvDirBaseError("Base path '{}' does not exist.".format(path))

    env_path = os.path.join(path, name)
    if does_path_exist(env_path):
        raise VenvDirBaseError(
            "Virtual environment '{}' already exists.".format(env_path)
        )
    create_venv(env_path, with_pip=True)
    config_parser.create_entry(name, path)


def add_entry(name, path):
    if not does_path_exist(path):
        raise VenvDirBaseError("Venv path '{}' does not exist.".format(path))
    config_parser.create_entry(name, path)


def get_entry(name):
    config_entry = config_parser.get_entry(name)
    return ManagedVirtualEnvironment(name, config_entry)


def remove_entry(name):
    entry = get_entry(name)
    remove_directory(entry.path)
    config_parser.remove_entry(name)
