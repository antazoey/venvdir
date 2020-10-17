import os
import venv
from configparser import ConfigParser

from util import get_user_project_path


def get_entries():
    accessor = _create_accessor()
    return accessor.entries


def create_entry(name, path=None):
    if not path:
        path = get_user_project_path("venvs")
    if not os.path.exists(path):
        raise Exception("Base path '{}' does not exist.".format(path))

    env_path = os.path.join(path, name)
    if os.path.exists(env_path):
        raise Exception("Virtual environment '{}' already exists.".format(env_path))
    venv.create(env_path, with_pip=True)


def _create_accessor():
    parser = ConfigParser
    return _EntryAccessor(parser)


class _EntryAccessor:
    ENTRIES_SECTION_KEY = "ENTRIES"
    DEFAULT_PATH = "."

    def __init__(self, parser):
        self.parser = parser
        file_name = "entries.cfg"
        self.path = os.path.join(get_user_project_path(), file_name)
        if not os.path.exists(self.path):
            self._init_entries_section()
            self._save()
        else:
            self.parser.read(self.path)

    @property
    def entries(self):
        try:
            return self.parser[self.ENTRIES_SECTION_KEY]
        except KeyError:
            self._init_entries_section()
            return self.parser[self.ENTRIES_SECTION_KEY]

    def _init_entries_section(self):
        self.parser.add_section(self.ENTRIES_SECTION_KEY)
        self.parser[self.ENTRIES_SECTION_KEY] = {}

    def _save(self):
        with open(self.path, "w+", encoding="utf-8") as file:
            self.parser.write(file)
