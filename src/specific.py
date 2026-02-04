"""Module specific.py"""
import argparse

import src.functions.cache


class Specific:
    """
    Specific
    """

    def __init__(self):
        """
        Constructor
        """

        self.__cache = src.functions.cache.Cache()

    @staticmethod
    def codes(value: str=None) -> list[int] | None:
        """

        :param value:
        :return:
        """

        if value is None:
            return None

        # Split and strip
        elements = [e.strip() for e in value.split(',')]

        try:
            _codes = [int(element) for element in elements]
        except argparse.ArgumentTypeError as err:
            raise err from err

        return _codes
