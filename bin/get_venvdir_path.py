#!/usr/bin/env python3
import sys
from venvdir.venvs import get_entry
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing name.\n\nUsage: \n\tget_vendir_path.py <venv-name>")
        exit(1)
    name = sys.argv[1]
    try:
        entry = get_entry(name)
        print(entry.path)
    except Exception as ex:
        print(str(ex))
