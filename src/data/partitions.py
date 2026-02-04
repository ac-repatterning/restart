"""Module partitions.py"""

import pandas as pd

import src.elements.partitions as prt


class Partitions:
    """
    Partitions for parallel computation.
    """

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__data = data

        # Fields
        self.__fields = ['ts_id', 'catchment_id', 'starting', 'ending']

    def __get_partitions(self) -> list[prt.Partitions]:
        """

        :return:
        """

        data = self.__data.copy()
        data = data.assign(
            starting = data['from'].apply(lambda x: x.strftime('%Y-%m-%d')),
            ending=data['to'].apply(lambda x: x.strftime('%Y-%m-%d')))

        records: pd.DataFrame = data[self.__fields]
        objects: pd.Series = records.apply(lambda x: prt.Partitions(**dict(x)), axis=1)

        return objects.tolist()

    def exc(self) -> list[prt.Partitions]:
        """

        :return:
        """

        return self.__get_partitions()
