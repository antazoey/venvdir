#!/usr/bin/env python3
import sys
from venvdir.venvs import get_entry


def get_path():
    name = sys.argv[1]
    entry = get_entry(name)
    print(entry.path)


if __name__ == "__main__":
    get_path()
