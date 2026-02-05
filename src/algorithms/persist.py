"""Module persist.py"""
import os

import pandas as pd
import src.functions.streams


class Persist:
    """
    Saves data files by year
    """

    def __init__(self, data: pd.DataFrame, catchment_id: int, ts_id: int):
        """

        :param data: A raw time series data set of a gauge station
        :param catchment_id:
        :param ts_id:
        """

        self.__data = data

        # Streams
        self.__streams = src.functions.streams.Streams()

        # Storage
        self.__path = os.path.join(os.getcwd(), str(catchment_id), str(ts_id))
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

        states: list[str] = [self.__persist(group = group) for group in self.__data['group'].unique()]

        return states
