"""Module interface.py"""
import datetime
import logging
import os.path

import pandas as pd

import config
import src.data.codes
import src.data.partitions
import src.data.points
import src.functions.directories
import src.functions.streams


class Interface:
    """
    Interface
    """

    def __init__(self, attributes: dict):
        """

        :param attributes: A set of data acquisition attributes.
        """

        self.__attributes = attributes

        # An instance for reading & writing CSV (comma separated values) data files.
        self.__streams = src.functions.streams.Streams()

        # the references directory
        self.__references_ = config.Config().references_
        directories = src.functions.directories.Directories()
        directories.create(path=self.__references_)

    def __persist(self, blob: pd.DataFrame, name: str) -> None:
        """

        :param blob:
        :param name:
        :return:
        """

        message = self.__streams.write(blob=blob, path=os.path.join(self.__references_, f'{name}.csv'))
        logging.info(message)

    def __span(self, assets: pd.DataFrame) -> pd.DataFrame:
        """

        :param assets:
        :return:
        """

        starting = datetime.datetime.strptime(self.__attributes.get('starting'), '%Y-%m-%d')

        if self.__attributes.get('reacquire'):
            at_least = datetime.datetime.strptime(self.__attributes.get('at_least'), '%Y-%m-%d')
        else:
            at_least = datetime.datetime.strptime(self.__attributes.get('ending'), '%Y-%m-%d')

        conditionals = (assets['from'] <= starting) & (assets['to'] >= at_least)
        assets = assets.loc[conditionals, :]

        return assets

    def __specific(self, assets: pd.DataFrame) -> pd.DataFrame:
        """

        :param assets:
        :return:
        """

        if self.__attributes.get('excerpt') is None:
            return pd.DataFrame()

        assets = assets.loc[assets['ts_id'].isin(self.__attributes.get('excerpt')), :]

        return assets

    def exc(self):
        """

        :return:
        """

        # Assets that have points that span a core period.
        assets = pd.DataFrame()
        assets = self.__span(assets=assets.copy())

        # If not starting from scratch
        if not self.__attributes.get('reacquire'):
            assets = self.__specific(assets=assets.copy())

        # Empty
        if assets.empty:
            return False

        # Partitions for parallel data retrieval; for parallel computing.
        partitions = src.data.partitions.Partitions(data=assets).exc(attributes=self.__attributes)
        logging.info(partitions)

        # Retrieving time series points
        src.data.points.Points(period=self.__attributes.get('period')).exc(partitions=partitions)

        return True
