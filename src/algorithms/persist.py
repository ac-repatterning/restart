"""Module persist.py"""
import os

import pandas as pd

import config
import src.elements.partitions as prt
import src.functions.streams


class Persist:
    """
    Saves data files by year
    """

    def __init__(self, data: pd.DataFrame, partition: prt.Partitions):
        """

        :param data: A raw time series data set of a gauge station
        :param partition:
        """

        self.__data = data
        self.__partition = partition

        # Streams
        self.__streams = src.functions.streams.Streams()

        # Storage
        self.__path = os.path.join(
            config.Config().series_, str(self.__partition.catchment_id), str(self.__partition.ts_id))
        if not os.path.exists(path=self.__path):
            os.makedirs(self.__path)

    def __persist(self, group: int) -> str:
        """

        :param group: A calendar year value.
        :return:
        """

        section: pd.DataFrame = self.__data.loc[self.__data['group'] == group, :]
        blob = section.sort_values(by='timestamp', ignore_index=True)
        blob.drop(columns='group', inplace=True)

        return self.__streams.write(blob=blob, path=os.path.join(self.__path, f'{group}-01-01.csv'))

    def exc(self) -> list[str]:
        """

        :return:
        """

        if self.__data.empty:
            return [f'{self.__partition.ts_id}, {self.__partition.starting}: empty']

        states: list[str] = [f'{str(self.__partition.ts_id)}, ' + self.__persist(group = group)
                             for group in self.__data['group'].unique()]

        return states
