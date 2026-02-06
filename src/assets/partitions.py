"""Module partitions.py"""
import datetime

import dask
import pandas as pd

import src.elements.partitions as prt


class Partitions:
    """
    Partitions for parallel computation.
    """

    def __init__(self, assets: pd.DataFrame, arguments: dict):
        """

        :param assets:
        :param arguments:
        """

        self.__assets = assets
        self.__arguments = arguments

        # Fields
        self.__fields = ['ts_id', 'catchment_id', 'starting', 'ending']

        # Variables
        self.__year = datetime.datetime.now().year

    @dask.delayed
    def __get_partitions(self, metadata: pd.DataFrame) -> list[prt.Partitions]:
        """

        :param metadata:
        :return:
        """

        records: pd.DataFrame = metadata[self.__fields]
        objects: pd.Series = records.apply(lambda x: prt.Partitions(**dict(x)), axis=1)

        return objects.tolist()

    @dask.delayed
    def __get_metadata(self, instance: pd.Series):
        """

        :param instance: An instance of a dataframe
        :return:
        """

        __parts = range(instance['from'].year, self.__year, self.__arguments.get('period') - 1)
        starting = [f'{__part}-01-01' for __part in __parts]
        ending = [f'{__part + self.__arguments.get('period') - 1}-01-01' for __part in __parts]

        __metadata = pd.DataFrame(data={'starting': starting, 'ending': ending})
        __metadata['ts_id'] = instance['ts_id']
        __metadata['catchment_id'] = instance['catchment_id']

        return __metadata

    def exc(self) -> list[prt.Partitions]:
        """

        :return:
        """

        computations = []
        for _, instance in self.__assets.iterrows():
            metadata: pd.DataFrame = self.__get_metadata(instance=instance)
            partitions: list[prt.Partitions] = self.__get_partitions(metadata=metadata)
            computations.append(partitions)
        calculations = dask.compute(computations)[0]

        return sum(calculations, [])
