""" This module contains a function to get a logger."""
import logging


def get_logger(name: str):
    """This function is used to get a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # create a console handler and set its level to INFO
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create a formatter and add it to the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)

    # add the handler to the logger
    logger.addHandler(ch)

    return logger
