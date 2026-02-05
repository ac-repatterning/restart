"""Module partitions.py"""
import datetime

import dask
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

        # Variables
        self.__year = datetime.datetime.now().year
        self.__period = 10

    @dask.delayed
    def __get_partitions(self, instances: pd.DataFrame) -> list[prt.Partitions]:
        """
        
        :param instances:
        :return:
        """

        records: pd.DataFrame = instances[self.__fields]
        objects: pd.Series = records.apply(lambda x: prt.Partitions(**dict(x)), axis=1)

        return objects.tolist()

    @dask.delayed
    def __get_instances(self, x: pd.Series):
        """

        :param x:
        :return:
        """

        __parts = range(x['from'].year, self.__year, self.__period - 1)
        starting = [f'{__part}-01-01' for __part in __parts]
        ending = [f'{__part + self.__period - 1}-01-01' for __part in __parts]

        __data = pd.DataFrame(data={'starting': starting, 'ending': ending})
        __data['ts_id'] = x['ts_id']
        __data['catchment_id'] = x['catchment_id']

        return __data

    def exc(self) -> list[prt.Partitions]:
        """

        :return:
        """

        computations = []
        for i, x in self.__data.iterrows():
            instances: pd.DataFrame = self.__get_instances(x = x)
            partitions: list[prt.Partitions] = self.__get_partitions(instances=instances)
            computations.append(partitions)
        calculations = dask.compute(computations)[0]

        return sum(calculations, [])
