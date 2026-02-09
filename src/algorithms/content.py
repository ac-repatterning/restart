"""Module special.py"""
import json
import sys

import requests


class Content:
    """
    Special
    """

    def __init__(self, headers: dict):
        """

        :param headers: An access token header.
        """

        self.__headers = headers

    def __get_content(self, url: str) -> str:
        """

        :param url: A data set's uniform resource locator
        :return:
        """

        try:
            response = requests.get(url=url, headers=self.__headers, timeout=600)
            response.raise_for_status()
        except requests.exceptions.Timeout as err:
            raise err from err
        except Exception as err:
            raise err from err

        if response.status_code == 200:
            content = response.content.decode(encoding='utf-8')
            return content

        sys.exit(response.status_code)

    def exc(self, url: str) -> dict | list[dict]:
        """

        :param url: A data set's uniform resource locator
        :return:
        """

        content = self.__get_content(url=url)

        return json.loads(content)
