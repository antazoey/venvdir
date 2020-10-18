import os
import subprocess
from configparser import ConfigParser

from venvdir.util import get_user_project_path
from venvdir.util import get_default_venvs_path


class VenvsConfigParser:
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
            entry = dict(self.parser[name])
            return entry
        except KeyError:
            raise Exception("Entry '{}' does not exist.".format(name))

    def create_entry(self, name, path=None):
        path = path or get_default_venvs_path()
        self.parser.add_section(name)
        self.parser[name] = {}
        self.parser[name]["path"] = os.path.join(path, name)
        self._save()

    def remove_entry(self, name):
        self.parser.remove_section(name)

    def _save(self):
        with open(self.path, "w+", encoding="utf-8") as file:
            self.parser.write(file)


config_parser = VenvsConfigParser(ConfigParser())
