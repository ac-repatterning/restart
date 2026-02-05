
import dask
import boto3

import src.elements.partitions as prt
import src.algorithms.data


class Interface:

    def __init__(self, connector: boto3.session.Session):

        self.__connector = connector

    def exc(self, partitions: list[prt.Partitions]):

        __data = dask.delayed(src.algorithms.data.Data(connector=self.__connector).__call__)

        computations = []
        for partition in partitions:
            data = __data(ts_id=partition.ts_id, starting=partition.starting, ending=partition.ending)
