import logging
import sys
from datetime import datetime

from compact_json import EolStyle, Formatter
from rich.console import Console
from rich.logging import RichHandler

# ---------------------------------------------------------------------------- #

formatter = Formatter()
formatter.indent_spaces = 2
formatter.max_inline_complexity = 10
formatter.json_eol_style = EolStyle.LF

# ---------------------------------------------------------------------------- #


console = Console()

# ---------------------------------------------------------------------------- #


def get_logger(name):
    """This function is used to get a logger for a module."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # TODO: Add file handler

    console_handler = RichHandler(
        show_time=False, rich_tracebacks=True, console=console
    )
    console_handler.setLevel(logging.DEBUG)

    # create console handler and set level to DEBUG
    # console_handler = logging.StreamHandler(sys.stdout)
    # console_handler.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    # formatter = logging.Formatter("%(name)-20s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def remove_timezones_from_dict(data_dict):
    if isinstance(data_dict, dict):
        # If the value is a dictionary, recursively remove timezone from its values
        return {k: remove_timezones_from_dict(v) for k, v in data_dict.items()}
    if isinstance(data_dict, list):
        # If the value is a list, recursively remove timezone from its items
        return [remove_timezones_from_dict(v) for v in data_dict]
    if isinstance(data_dict, datetime):
        # If the value is a datetime with timezone information, convert it to a timezone-unaware datetime
        return data_dict.replace(tzinfo=None)
    return data_dict


def filter_and_sort_dict_list(dict_list, order):
    """
    Sort a list of dictionaries by a custom order based on the keys.

    Parameters:
        list_of_dicts (list): The list of dictionaries to sort.
        order (list): The list of keys in the desired order.

    Returns:
        list: A new list of dictionaries with the keys sorted in the custom order.
    """
    filtered_list = []

    for item in dict_list:
        sorted_dict = {key: item.get(key) for key in order}
        filtered_list.append(sorted_dict)

    return filtered_list
