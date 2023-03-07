""" Utility Functions - Shared Functions. """


import logging
from datetime import datetime

#
from rich.logging import RichHandler
from rich.traceback import install

install(show_locals=True, max_frames=2)


def get_logger(name):
    """This function is used to get a logger for a module."""

    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    handler = RichHandler(
        rich_tracebacks=True,
        show_time=True,
        show_level=True,
        show_path=True,
        markup=True,
        log_time_format="[%X]",
    )

    handler.rich_tracebacks = True

    # handler.formatter.datefmt = "%X"
    # formatter = logging.Formatter("%(message)s")

    # console_handler.setFormatter(formatter)
    # logger.addHandler(console_handler)

    # console_handler.setFormatter(formatter)
    logger.addHandler(handler)

    # logging.basicConfig(
    #     level="DEBUG",
    #     format="%(message)s",
    #     datefmt="[%X]",
    #     handlers=[RichHandler(rich_tracebacks=True)]
    # )

    # logger = logging.getLogger(name)

    return logger

    # log = logging.getLogger(name)

    # return log


# ---------------------------------------------------------------------------- #
def remove_timezones_from_object(  # pylint: disable=inconsistent-return-statements
    data_object,
):
    """Remove timezone information from a dictionary or list of dictionaries."""
    if isinstance(data_object, dict):
        # If the value is a dictionary, recursively remove timezone from its
        # values
        # type: ignore
        return {k: remove_timezones_from_object(v) for k, v in data_object.items()}

    if isinstance(data_object, list):
        # If the value is a list, recursively remove timezone from its items
        # type: ignore
        return [remove_timezones_from_object(v) for v in data_object]

    if isinstance(data_object, datetime):
        # If the value is a datetime with timezone information, convert it to a
        # timezone-unaware datetime
        return data_object.replace(tzinfo=None)  # type: ignore


def filter_and_sort_dict_list(dict_list, order):
    """Sort a list of dictionaries by a custom order based on the keys.

    Parameters
    ----------
        list_of_dicts (list): The list of dictionaries to sort.
        order (list): The list of keys in the desired order.

    Returns
    -------
        list: A new list of dictionaries with the keys sorted in the custom order.
    """
    filtered_list = []

    if dict_list is None:
        return dict_list

    for item in dict_list:
        sorted_dict = {key: item.get(key) for key in order}
        filtered_list.append(sorted_dict)

    return filtered_list


# ---------------------------------------------------------------------------- #

# pprint(["eggs", "ham"], expand_all=True)
# pprint(locals(), max_length=2)
# pprint("Where there is a Will, there is a Way", max_string=21)


# class Bird:
#     def __init__(self, name, eats=None, fly=True, extinct=False):
#         self.name = name
#         self.eats = list(eats) if eats else []
#         self.fly = fly
#         self.extinct = extinct

#     def __repr__(self):
#         return f"Bird({self.name!r}, eats={self.eats!r}, fly={self.fly!r}, extinct={self.extinct!r})"

#     def __rich_repr__(self):
#         yield self.name
#         yield "eats", self.eats
#         yield "fly", self.fly, True
#         yield "extinct", self.extinct, False

#     BIRDS = {
# "gull": Bird("gull", eats=["fish", "chips", "ice cream", "sausage rolls"]),
# "penguin": Bird("penguin", eats=["fish"], fly=False),
# "dodo": Bird("dodo", eats=["fruit"], fly=False, extinct=True)
# }


# print(repr(BIRDS["gull"]))
# print(BIRDS["gull"])

# @rich.repr.auto
# @rich.repr.auto(angular=True)
# class Bird:
#     def __init__(self, name, eats=None, fly=True, extinct=False):
#         self.name = name
#         self.eats = list(eats) if eats else []
#         self.fly = fly
#         self.extinct = extinct


# import boto3
# # import logging
# # from rich.logging import RichHandler

# logging.basicConfig(
#     level="NOTSET",
#     format="%(message)s",
#     datefmt="[%X]",
#     handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[boto3])]
# )

# log = logging.getLogger("rich")
# try:
#     print(1 / 0)
# except Exception:
#     log.exception("unable print!")
