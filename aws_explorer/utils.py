import logging
import sys
from datetime import datetime
from typing import Dict, List


def get_logger(name):
    """This function is used to get a logger for a module."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to DEBUG
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(name)-20s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def remove_timezones_from_object(data_object):
    if isinstance(data_object, dict):
        # If the value is a dictionary, recursively remove timezone from its values
        return {k: remove_timezones_from_object(v) for k, v in data_object.items()}  # type: ignore

    if isinstance(data_object, list):
        # If the value is a list, recursively remove timezone from its items
        return [remove_timezones_from_object(v) for v in data_object]  # type: ignore

    if isinstance(data_object, datetime):
        # If the value is a datetime with timezone information, convert it to a timezone-unaware datetime
        return data_object.replace(tzinfo=None)  # type: ignore


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

    if dict_list is None:
        return dict_list

    for item in dict_list:
        sorted_dict = {key: item.get(key) for key in order}
        filtered_list.append(sorted_dict)

    return filtered_list
