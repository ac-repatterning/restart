"""Module specific.py"""
import argparse
import logging
import src.functions.cache


class Specific:
    """
    Specific
    """

    def __init__(self):

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

    def reacquire(self, value: str='0') -> bool:
        """

        :param value:
        :return:
        """

        try:
            _value = int(value)
        except argparse.ArgumentTypeError as err:
            logging.info(('The optional parameter --reacquire expects an integer; '
                          '0 indicates false, i.e., do not reacquire, and '
                          '1 or != 0 indicates true, i.e., reacquire'))
            self.__cache.exc()
            raise err from err

        return False if _value == 0 else True
