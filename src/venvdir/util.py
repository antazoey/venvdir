from collections import OrderedDict
from os import makedirs
from os import path

_PADDING_SIZE = 3


def get_user_project_path(*sub_dirs):
    """The path on your user dir to /.venvdir. Will create if not exists."""
    package_name = __name__.split(".")[0]
    home = path.expanduser("~")
    hidden_package_name = ".{}".format(package_name)
    user_project_path = path.join(home, hidden_package_name)
    result_path = path.join(user_project_path, *sub_dirs)
    if not path.exists(result_path):
        makedirs(result_path)
    return result_path


def format_to_table(rows, column_size):
    """Formats given rows into a string of left justified table."""
    lines = []
    for row in rows:
        line = ""
        for key in row.keys():
            line += str(row[key]).ljust(column_size[key] + _PADDING_SIZE)
        lines.append(line)
    return "\n".join(lines)


def find_format_width(record):
    """Fetches needed keys/items to be displayed based on header keys.

    Finds the largest string against each column so as to decide the padding size for the column.

    Args:
        record (dict): data to be formatted.

    Returns:
        tuple (list of dict, dict): Ordered records, padding size of columns mapped to names.
    """
    rows = []
    # noinspection PyTypeChecker
    max_width_item = dict(record.items())  # Copy
    for record_row in record:
        row = OrderedDict()
        for header_key in record.keys():
            item = record_row.get(header_key)
            row[header_key] = item
            max_width_item[header_key] = max(max_width_item[header_key], str(item), key=len)
        rows.append(row)
    column_size = {key: len(value) for key, value in max_width_item.items()}
    return rows, column_size


def _get_default_header(header_items):
    if not header_items:
        return

    # Creates dict where keys and values are the same for `find_format_width()`.
    header = {}
    for item in header_items:
        keys = item.keys()
        for key in keys:
            if key not in header and isinstance(key, str):
                header[key] = key
    return header